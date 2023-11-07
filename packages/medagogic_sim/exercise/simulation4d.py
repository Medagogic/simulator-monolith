from __future__ import annotations
import datetime
import os
import traceback
from typing import TYPE_CHECKING, Optional
from pydantic import BaseModel
from abc import ABC, abstractmethod, abstractproperty
import json
from typing import Any, Dict, List
import markdown_to_json
import asyncio
from rx.subject import Subject

from packages.medagogic_sim.gpt import MODEL_GPT4, gpt, UserMessage, SystemMessage, GPTMessage, MODEL_GPT35
from packages.medagogic_sim.exercise.markdownexercise import HEADER_EVENTS, MarkdownExercise, VitalSigns, VitalSignsInterpolation
from packages.medagogic_sim.exercise.simulation_types import Vitals, abcde_list_to_dict, vitals_list_to_dict
from packages.medagogic_sim.history.sim_history import Evt_CompletedIntervention


if TYPE_CHECKING:
    from packages.medagogic_sim.history.sim_history import HistoryLog
    
from packages.medagogic_sim.logger.logger import get_logger, logging
logger = get_logger(level=logging.INFO)


def log_error_with_traceback(e):
    tb_str = traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)
    tb_str = ''.join(tb_str)
    logging.error(f"Error processing updates: {e}\n{tb_str}")

class SimulationUpdateReciept:
    id: str
    on_new_immediate_state_generated = Subject()
    on_finished = Subject()
    finished: bool = False

    def finish(self):
        self.finished = True
        self.on_finished.on_next(None)


class NewCurrentStateResponse(BaseModel):
    gpt_messages: List[Dict]
    gpt_response: str
    new_current_state_markdown: str

class NewStateProgressionResponse(BaseModel):
    gpt_messages: List[Dict]
    gpt_response: str
    new_state_progression_markdown: str

class ValueDiff(BaseModel):
    old: Any
    new: Any

class SimulationUpdateDiff(BaseModel):
    vitals: Dict[Vitals, ValueDiff]
    abcde: Dict[str, ValueDiff]
    future_vitals: Dict[Vitals, ValueDiff]
    future_abcde: Dict[str, ValueDiff]

class SimulationUpdateLog:
    def __init__(self,
        previous_exercise: MarkdownExercise,
        new_current_state_response: NewCurrentStateResponse,
        new_state_progression_response: NewStateProgressionResponse,
        new_exercise: MarkdownExercise
    ) -> None:
        self.previous_exercise = previous_exercise
        self.new_current_state_response = new_current_state_response
        self.new_state_progression_response = new_state_progression_response
        self.new_exercise = new_exercise

    def get_changes(self) -> SimulationUpdateDiff:
        previous_exercise = self.previous_exercise
        updated_exercise = self.new_exercise

        vitals: Dict[Vitals, ValueDiff] = {}
        abcde: Dict[str, ValueDiff] = {}
        future_vitals: Dict[Vitals, ValueDiff] = {}
        future_abcde: Dict[str, ValueDiff] = {}

        for vitals_key, previous_value in previous_exercise.current_state.vital_signs.dict().items():
            new_value = updated_exercise.current_state.vital_signs.dict()[vitals_key]
            if new_value != previous_value:
                vitals[vitals_key] = ValueDiff(old=previous_value, new=new_value)   # type: ignore
        
        for abcde_key, previous_value in previous_exercise.current_state.abcde.to_dict().items():
            new_value = updated_exercise.current_state.abcde.to_dict()[abcde_key]
            if new_value != previous_value:
                abcde[abcde_key] = ValueDiff(old=previous_value, new=new_value)
        
        for vitals_key, previous_value in previous_exercise.progression.vitals.items():
            new_value = updated_exercise.progression.vitals[vitals_key]
            if new_value != previous_value:
                future_vitals[vitals_key] = ValueDiff(old=str(previous_value), new=str(new_value))

        for abcde_key, previous_value in previous_exercise.progression.abcde.items():
            new_value = updated_exercise.progression.abcde[abcde_key]
            if new_value != previous_value:
                future_abcde[abcde_key] = ValueDiff(old=previous_value, new=new_value)
        
        return SimulationUpdateDiff(
            vitals=vitals,
            abcde=abcde,
            future_vitals=future_vitals,
            future_abcde=future_abcde
        )
    
    def save(self):
        diff = self.get_changes()

        output_dict = {
            "previous_exercise": self.previous_exercise.to_markdown(),
            "new_current_state_response": self.new_current_state_response.dict(),
            "new_state_progression_response": self.new_state_progression_response.dict(),
            "new_exercise": self.new_exercise.to_markdown(),
            "diff": diff.dict()
        }

        # output_filename is the folder of this file + "/logs/simulation_updates/" + datetime.now().isoformat() + ".json"
        output_folder = os.path.join(os.path.dirname(__file__), "logs/simulation_updates")
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        output_filename = f"{output_folder}/{datetime.datetime.now().isoformat()}.json"
        with open(output_filename, "w") as f:
            f.write(json.dumps(output_dict, indent=4))


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


class TimeKeeper:
    def __init__(self) -> None:
        self.time = 0

        async def loop():
            while True:
                await asyncio.sleep(1)
                self.time += 1

        self.loop = asyncio.create_task(loop())

    @property
    def exerciseTimeSeconds(self) -> float:
        return self.time



class LeafyBlossom(IBlackBoxSimulation):
    def __init__(self, exercise: MarkdownExercise, history_log: HistoryLog) -> None:
        self.exercise = exercise
        self.timekeeper = TimeKeeper()

        self.history_log = history_log
        self.interpolation_start_time: float = 0
        self.vitals_interpolation = self.resetInterpolation()
        self.pending_updates: List[str] = []
        self.pending_reciepts: List[SimulationUpdateReciept] = []
        self.finished = False
        self.loop = asyncio.create_task(self.__loop())
        self.on_alert = Subject()
        self.gpt_model = MODEL_GPT4
        self.on_state_change = Subject()


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
                try:
                    await self.process_updates()
                except Exception as e:
                    log_error_with_traceback(e)
            else:
                await asyncio.sleep(1)
                

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


    def validate_update_markdown(self, update_markdown: str) -> Optional[str]:
        try:
            state_update_dict = markdown_to_json.dictify(update_markdown)
            if "Current Patient State" in state_update_dict:
                state_update_dict = state_update_dict["Current Patient State"]
            elif "State Progression" in state_update_dict:
                state_update_dict = state_update_dict["State Progression"]
            else:
                return f"Invalid update markdown (no state progression or current patient state): {update_markdown}"
        except Exception as e:
            logger.error(f"Error validating update markdown: {e}")
            return f"Invalid update markdown: {update_markdown}"
        
        return None


    def apply_update_markdown(self, exercise: MarkdownExercise, update_markdown: str, future_state: bool = False) -> MarkdownExercise:
        state_update_dict = markdown_to_json.dictify(update_markdown)
        if "Current Patient State" in state_update_dict:
            state_update_dict = state_update_dict["Current Patient State"]
        elif "State Progression" in state_update_dict:
            state_update_dict = state_update_dict["State Progression"]
        else:
            logger.error(update_markdown)
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
            self.on_alert.on_next(state_update_dict["Alert"])

        self.on_state_change.on_next(exercise)

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

        new_current_state_data = await self.calculate_new_current_state(updated_exercise, update_text)
        current_state_update_markdown = new_current_state_data.new_current_state_markdown

        updated_exercise = self.apply_update_markdown(updated_exercise, current_state_update_markdown, future_state=False)

        for pending_reciept in reciepts:
            pending_reciept.on_new_immediate_state_generated.on_next((updated_exercise, current_state_update_markdown))

        new_state_progression_data = await self.calculate_new_state_progression(updated_exercise, update_text)
        future_state_update_markdown = new_state_progression_data.new_state_progression_markdown
        try:
            updated_exercise = self.apply_update_markdown(updated_exercise, future_state_update_markdown, future_state=True)
        except Exception as e:
            logger.error(f"Error applying future state update: {e}")
            log_error_with_traceback(e)
            logger.error(future_state_update_markdown)
        
        update_log = SimulationUpdateLog(
            previous_exercise=self.exercise,
            new_current_state_response=new_current_state_data,
            new_state_progression_response=new_state_progression_data,
            new_exercise=updated_exercise
        )
        update_log.save()

        self.exercise = updated_exercise
        self.resetInterpolation()

        logger.info(f"Finished processing updates: {updates_cache}")

        # for update in updates_cache:
        #     # self.intervention_tracker.recordEvent(self.simulationTimeSeconds, update)
        #     self.history_log.add_event(Intervention(npc_name="", content=update))

        for pending_reciept in reciepts:
            pending_reciept.finish()


    def get_state_markdown(self, exercise: MarkdownExercise, include_progression: bool) -> str:
        completed_interventions_text = "No significant events yet."
        if len(self.history_log.get_filtered_log(filter_types=[Evt_CompletedIntervention])) > 0:
            completed_interventions_text = self.history_log.get_markdown(filter_types=[Evt_CompletedIntervention])

        markdown = f"""
{exercise.to_markdown(include_progression=include_progression)}

# Simulation History
{completed_interventions_text}
""".strip()

        return markdown

    async def calculate_new_current_state(self, exercise: MarkdownExercise, update: str) -> NewCurrentStateResponse:
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

First, provide a description of what happens as an immediate consequence, including any relevant simulation/patient information. Ensure that you aren't thinking too far into the future - this should only be the immediate consequences (as in, within a few seconds) of the update. Write this as definites (ie "will"), not "coulds" or "mights". Keep this as brief as possible while containing all your thoughts and reasoning. It might also be useful to include a mention of parameters which will not change. Prefix these lines with // to denote them as comments.

Then, provide your updates. Use your description above when deciding on changes. This must match the format above, ie only giving the values.
        """
        logger.info(f"Calculating new immediate state from update: {update}")

        try:
            messages = [SystemMessage(prompt), UserMessage(update)]
            full_response = await gpt(messages, model=self.gpt_model, max_tokens=1000, temperature=0)
        except Exception as e:
            logger.error(f"Error calculating new immediate state from update: {e}")
            raise e

        logger.info(f"Calculated new immediate state from updte: {update}")

        update_markdown = full_response.strip()
        markdown_error = self.validate_update_markdown(update_markdown)
        if markdown_error is not None:
            logger.error(markdown_error)
            logger.error(update_markdown)
            exit()
            

        return NewCurrentStateResponse(
            gpt_messages=messages,  # type: ignore
            gpt_response=full_response,
            new_current_state_markdown=update_markdown
        )


    async def calculate_new_state_progression(self, exercise: MarkdownExercise, update: str):
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

        messages = [SystemMessage(prompt), UserMessage(content=update)]
        full_response = await gpt(messages, model=self.gpt_model, max_tokens=1000, temperature=0)

        logger.info(f"Calculated new future state progression from update: {update}")

        return NewStateProgressionResponse(
            gpt_messages=messages,  # type: ignore
            gpt_response=full_response,
            new_state_progression_markdown=full_response.strip()
        )


if __name__ == "__main__":
    DEBUG_LIVE_OUTPUT = False
    from packages.medagogic_sim.context_for_brains import ContextForBrains
    from packages.medagogic_sim.npcs.npc_manager import NPCManager
    from packages.medagogic_sim.npcs.the_brains import RightBrainDecision
    import asyncio

    async def main() -> None:
        context = ContextForBrains()
        sim: LeafyBlossom = context.simulation

        sim.gpt_model = MODEL_GPT35 # Just royally fuck it up

        sim.applyUpdate("Dr Johnson started Chin lift")
        await sim.process_updates()

        print("==================================================")
        print(sim.exercise.to_markdown())
        print("==================================================")
        exit()

        states = {}

        elapsed_time = 0

        while len(states.keys()) < 30:
            print(f"@ {elapsed_time} seconds")
            currentState = sim.getCurrentVitals().dict()
            print(json.dumps(currentState, indent=4))

            states[elapsed_time] = currentState

            with open(f"autosim/simulation_services/v3_leafyblossom/simulated_states.json", "w") as f:
                f.write(json.dumps(states, indent=4))

            await asyncio.sleep(5)
            elapsed_time += 5

            if elapsed_time >= 30 and elapsed_time < 35:
                sim.__add_update("20l oxygen given at 15l/min via non-rebreather mask")
            elif elapsed_time >= 60 and elapsed_time < 65:
                sim.__add_update("220mg paracetamol has been administered intravenously")
        

    asyncio.run(main())