from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from simulation_time_keeper import ISimulationTimeKeeper
    from intervention_tracker import InterventionTracker

from abc import ABC, abstractmethod, abstractproperty
from typing import Any, Dict, List
import markdown_to_json
from packages.server.gpt.gpt_api import GPTMessage, MODEL_GPT4, Role, gpt
import asyncio
from packages.server.sim_app.med_sim.markdownexercise import HEADER_EVENTS, MarkdownExercise, VitalSigns, VitalSignsInterpolation
from packages.server.sim_app.util.logger import get_logger

from rx.subject import Subject

import logging
from packages.server.sim_app.med_sim.simulation_types import Vitals, abcde_list_to_dict, vitals_list_to_dict

logger = get_logger(level=logging.INFO)


DEBUG_LIVE_OUTPUT = False


class SimulationUpdateReciept:
    id: str
    on_current_state_calculated = Subject()
    on_processed = Subject()


class IBlackBoxSimulation(ABC):
    @abstractmethod
    def getCurrentVitals(self) -> VitalSigns:
        pass

    @abstractmethod
    def applyUpdate(self, update: str) -> SimulationUpdateReciept:
        pass

    @abstractproperty
    def simulationTimeSeconds(self) -> float:
        pass

    @abstractmethod
    def getExercise(self) -> MarkdownExercise:
        pass

    @abstractmethod
    def get_immediate_markdown(self) -> str:
        pass

class LeafyBlossom(IBlackBoxSimulation):
    def __init__(self, exercise_path: str, timekeeper: ISimulationTimeKeeper, intervention_tracker: InterventionTracker) -> None:
        self.exercise_name = exercise_path
        self.timekeeper: ISimulationTimeKeeper = timekeeper
        self.exercise = MarkdownExercise.from_markdown(self.__open_exercise(exercise_path))
        self.intervention_tracker = intervention_tracker
        self.interpolation_start_time: float = 0
        self.vitals_interpolation = self.resetInterpolation()
        self.pending_updates: List[str] = []
        self.pending_reciepts: List[SimulationUpdateReciept] = []
        self.finished = False
        self.loop = asyncio.create_task(self.__loop())


    def getCurrentVitals(self, seconds_in_future: float = 0) -> VitalSigns:
        elapsed_time_seconds = (self.simulationTimeSeconds + seconds_in_future) - self.interpolation_start_time
        return self.vitals_interpolation.interpolate(elapsed_time_seconds / 60)
    

    def applyUpdate(self, update: str) -> SimulationUpdateReciept:
        self.__add_update(update)
        reciept = SimulationUpdateReciept()
        self.pending_reciepts.append(reciept)
        return reciept


    @property
    def simulationTimeSeconds(self) -> float:
        return self.timekeeper.exerciseTimeSeconds
    
    
    def getExercise(self) -> MarkdownExercise:
        return self.exercise


    async def __loop(self):
        while not self.finished:
            if len(self.pending_updates) > 0:
                await self.process_updates()
            else:
                await asyncio.sleep(1)


    def __open_exercise(self, path: str) -> str:
        with open(path, "r") as f:
            return f.read()

    def resetInterpolation(self):
        logger.info("Resetting interpolation")
        self.vitals_interpolation = VitalSignsInterpolation(self.exercise.current_state.vital_signs, self.exercise.progression)
        self.interpolation_start_time = self.simulationTimeSeconds
        return self.vitals_interpolation


    def __add_update(self, update_text: str) -> None:
        self.pending_updates.append(update_text)


    def get_immediate_markdown(self) -> str:
        current_exercise = MarkdownExercise.from_markdown(self.exercise.to_markdown())
        current_exercise.current_state.vital_signs = self.getCurrentVitals(seconds_in_future=7)
        return current_exercise.to_markdown(include_progression=False)
    

    def __alert(self, message: str) -> None:
        logger.log(logging.INFO, f"ALERT: {message}")


    def apply_update_markdown(self, exercise: MarkdownExercise, update_markdown: str, future_state: bool = False) -> MarkdownExercise:
        state_update_dict = markdown_to_json.dictify(update_markdown)
        if "Current Patient State" in state_update_dict:
            state_update_dict = state_update_dict["Current Patient State"]
        elif "State Progression" in state_update_dict:
            state_update_dict = state_update_dict["State Progression"]
        else:
            raise ValueError("Invalid update markdown (no state progression or current patient state)")

        if "Vital Signs" in state_update_dict:
            vitals_update_dict = state_update_dict["Vital Signs"]
            timed_vitals = vitals_list_to_dict(vitals_update_dict)
            if future_state:
                exercise.progression.update_vitals(timed_vitals)
            else:
                untimed_vitals: Dict[Vitals, Any] = {}
                for k, v in timed_vitals.items():
                    untimed_vitals[k] = v.value
                exercise.current_state.vital_signs.update_from_dict(untimed_vitals)
        if "ABCDE" in state_update_dict:
            abcde_update_list = state_update_dict["ABCDE"]
            abcde_update_dict = abcde_list_to_dict(abcde_update_list)
            if future_state:
                exercise.progression.update_abcde(abcde_update_dict)
            else:
                exercise.current_state.abcde.update_from_dict(abcde_dict=abcde_update_dict)
        if future_state and HEADER_EVENTS in state_update_dict:
            exercise.progression.events = state_update_dict[HEADER_EVENTS]
        if "Alert" in state_update_dict:
            self.__alert(state_update_dict["Alert"])

        return exercise

    async def process_updates(self) -> None:
        if len(self.pending_updates) == 0:
            return
        
        reciepts = self.pending_reciepts
        self.pending_reciepts = []
        
        logger.log(logging.INFO, f"Processing updates: {self.pending_updates}")

        updates_cache = self.pending_updates.copy()
        self.pending_updates = []

        update_text = ""
        for update in updates_cache:
            update_text += f"\n- {update}"
        update_text = update_text.strip()

        updated_exercise = MarkdownExercise.from_markdown(self.exercise.to_markdown())

        updated_exercise.current_state.vital_signs = self.getCurrentVitals(seconds_in_future=15)

        current_state_update_markdown = await self.__get_new_current_state(updated_exercise, update_text)
        updated_exercise = self.apply_update_markdown(updated_exercise, current_state_update_markdown, future_state=False)

        for pending_reciept in reciepts:
            pending_reciept.on_current_state_calculated.on_next(updated_exercise)

        future_state_update_markdown = await self.__get_new_state_progression(updated_exercise, update_text)
        try:
            updated_exercise = self.apply_update_markdown(updated_exercise, future_state_update_markdown, future_state=True)
        except Exception as e:
            logger.log(logging.ERROR, f"Error applying future state update: {e}")

        for vitals_key, v in self.exercise.current_state.vital_signs.dict().items():
            if updated_exercise.current_state.vital_signs.dict()[vitals_key] != v:
                logger.log(logging.INFO, f"CURRENT: {vitals_key}\n\t\tOld:{v}\n\t\tNew {updated_exercise.current_state.vital_signs.dict()[vitals_key]}")
        
        for abcde_key, v in self.exercise.current_state.abcde.to_dict().items():
            if updated_exercise.current_state.abcde.to_dict()[abcde_key] != v:
                logger.log(logging.INFO, f"CURRENT: {abcde_key}\n\t\tOld: {v}\n\t\tNew: {updated_exercise.current_state.abcde.to_dict()[abcde_key]}")
        
        for vitals_key, v in self.exercise.progression.vitals.items():
            if updated_exercise.progression.vitals[vitals_key] != v:
                logger.log(logging.INFO, f"FUTURE: {vitals_key}\n\t\tOld: {v}\n\t\tNew: {updated_exercise.progression.vitals[vitals_key]}")

        for abcde_key, v in self.exercise.progression.abcde.items():
            if updated_exercise.progression.abcde[abcde_key] != v:
                logger.log(logging.INFO, f"FUTURE: {abcde_key}\n\t\tOld: {v}\n\t\tNew: {updated_exercise.progression.abcde[abcde_key]}")
        
        self.exercise = updated_exercise
        self.resetInterpolation()

        for pending_reciept in reciepts:
            pending_reciept.on_processed.on_next(self)


    def get_state_markdown(self, exercise: MarkdownExercise, include_progression: bool) -> str:
        completed_interventions_text = "No significant events yet."
        if len(self.intervention_tracker.events) > 0:
            completed_interventions_text = self.intervention_tracker.to_markdown(self.timekeeper.exerciseTimeSeconds)

        markdown = f"""
{exercise.to_markdown(include_progression=include_progression)}

# Simulation History
{completed_interventions_text}
""".strip()

        return markdown


    async def __get_new_current_state(self, exercise: MarkdownExercise, update: str):
        prompt = f"""
{self.get_state_markdown(exercise, include_progression=False)}

==================================================

# Instructions
You are to provide an updated version of the above data based on the following update. Do not provide any other information.
Ensure that all consequences of the update are included in the updated data, and that all changes are medically accurate.
You MUST include all changes to values, vital signs, ABCDEs, etc.
Provide updates for ONLY the following sections:

- Vital Signs
- ABCDE

You must conform to the structure of the existing sections, and you may not add new sub-sections.
You may only provide updates for the above sections, and you may not provide updates for any other sections.
Only make modifications which would happen immediately, as a direct result of the update, within the first 5-10 seconds.
Do not make any changes which would take longer than 10 seconds to occur. Ensure medical accuracy.
These values will also change over time, handled by a separate system. You do not need to worry about this.
Ensure that the changes are medically accurate based on all available data.
Only make modifications which would realistically happen as a direct result of the given update, do not invent, imagine, or assume any information.

Provide updates for:
- Current Patient State

DO NOT PROVIDE LINES WHICH YOU ARE NOT CHANGING. ONLY PROVIDE LINES WHICH YOU ARE CHANGING. SKIP THESE SUB-SECTIONS FROM THE RESPONSE.
YOU MUST PROVIDE A FULL DESCRIPTION OF THE CURRENT STATE FOR EACH SUB-SECTION YOU ARE MODIFIYING (ie include info from the old state too).

First, provide a description of what you expect to happen immediately, including all relevant medical information. Ensure that you aren't thinking too far into the future - this should only be the immediate consequences (as in, within a few seconds) of the update. Write this as definites (ie "will"), not "coulds" or "mights". Keep this as brief as possible while containing all your thoughts and reasoning. It might also be useful to include a mention of parameters which will not change.

Then, provide your updates. Use your description above when deciding on changes. This must match the format above, ie only giving the values.

Additionally, you may provide an **Alert** notification if a significant event has occured following this update, for a doctor or nurse in the room to notice and react to. Do this in the following format:

# Alert
- The patient has begun to bleed from the nose.
        """
        logger.info(f"Calculating new immediate state from update: {update}")

        messages = [GPTMessage(role=Role.SYSTEM, content=prompt), GPTMessage(role=Role.USER, content=update)]
        full_response = await gpt(messages, model=MODEL_GPT4+"-0613", max_tokens=1000, temperature=0, top_p=1, show_progress=False)

        logger.info(f"Immediate state update response: {full_response}")

        return full_response.strip()



    async def __get_new_state_progression(self, exercise: MarkdownExercise, update: str):
        prompt = f"""
{self.get_state_markdown(exercise, include_progression=True)}

==================================================

# Instructions
You are to provide an updated version of the above data based on the following update. Do not provide any other information.
Ensure that all consequences of the update are included in the updated data, and that all changes are medically accurate.
You MUST include all changes to values, vital signs, ABCDEs, etc. These values will be interpolated by an external program.
Provide updates for ONLY the following sections:

- {HEADER_EVENTS}
- Vital Signs
- ABCDE

You must conform to the structure of the existing sections, and you may not add new sub-sections.
You may only provide updates for the above sections, and you may not provide updates for any other sections.
Ensure that the changes are medically accurate based on all available data.
Pick times for each progression variable which are medically accurate. The times for each element may be different.

Provide updates for:
- State Progression

DO NOT PROVIDE VALUES WHICH YOU ARE NOT CHANGING. ONLY PROVIDE VALUES WHICH ARE CHANGING. SKIP THESE SUB-SECTIONS FROM THE RESPONSE.
YOU MUST PROVIDE A FULL DESCRIPTION OF THE DESIRED STATE PROGRESSION FOR EACH SUB-SECTION YOU ARE MODIFIYING (ie include info from the old state progression too)
If there is to be no change over time from the current state, then you can simply write "No change from current state" for that variable.
Any of the existing ABCDE state progressions which are unaffected by this update must be included in your response.

======================

Examples:

** Example 1 **
If oxygen is given when saturation is currently low, the current o2 saturation should rise slightly, and the future saturation should give a quick rise over the next 30 seconds (assuming there is nothing contradictory in the current state). There may be some additional effects as other systems have sympathetic responses, for example the breathing rate and heart rate may show some slight variation.

** Example 2 **
If paracetamol is given, the current temperature will likely not change due to the drug taking some time to take effect. The temperature would drop slowly (over the next 10-15 minutes) to a lower level.

** Example 3 **
There may be complex scenarios where some variable is rising due to an underlying cause, and a drug is given to counteract this. In this case, the variable may continue to rise for a short time, before dropping. You will need to consider the effects of the drug, and the effects of the underlying cause, and the time it takes for the drug to take effect.

** Example 4 **
The patient's current disability is P on AVPU scale (responds to pain stimuli), and pupils are normal. An intervention is made which results in the pupils becoming dilated over the next 3 minutes, but no change in the AVPU status. Your response must include both the AVPU status and the pupil status, rather than just the pupil status.

** Note **
Each vital sign may only have a single progression (ie you may not list multiple time points)

======================

First, provide a description of what you expect to happen as a result of the updates, including all relevant medical information. Ensure that you aren't thinking too far into the future of the update (ie no more than 10-15 minutes). Write this as definites (ie "will"), not "coulds" or "mights". Keep this as brief as possible while containing all your thoughts and reasoning. It might also be useful to include a mention of parameters which will not change.
        """
        logger.info(f"Calculating new future state from update: {update}")

        messages = [GPTMessage(role=Role.SYSTEM, content=prompt), GPTMessage(role=Role.USER, content=update)]
        full_response = await gpt(messages, model=MODEL_GPT4+"-0613", max_tokens=1000, temperature=0, top_p=1, show_progress=False)

        logger.info(f"Got response for future progress: {full_response}")

        return full_response.strip()


if __name__ == "__main__":
    DEBUG_LIVE_OUTPUT = False
    import asyncio
    from simulation_time_keeper import DummyTimeKeeper
    from intervention_tracker import InterventionTracker

    async def main():
        timekeeper = DummyTimeKeeper()
        intervention_tracker = InterventionTracker()


        sim = LeafyBlossom("packages/server/sim_app/med_sim/exercises/pediatric_septic_shock.txt",
                           timekeeper=timekeeper, 
                           intervention_tracker=intervention_tracker)

        sim.applyUpdate("Dr Johnson started oxygen at 15l/min via non-rebreather mask")
        await sim.process_updates()

        print(sim.exercise.to_markdown())
        exit()


    asyncio.run(main())