from __future__ import annotations
import asyncio
from typing import Any, TYPE_CHECKING, Coroutine, List, Optional, Tuple
from rx.subject import Subject
from packages.medagogic_sim.exercise.simulation4d import SimulationUpdateReciept

from packages.medagogic_sim.exercise.simulation_types import ActionType

if TYPE_CHECKING:
    from packages.medagogic_sim.actions_for_brains import TaskCall
    from packages.medagogic_sim.exercise.markdownexercise import MarkdownExercise
    from packages.medagogic_sim.npc import MedicalNPC
    from packages.medagogic_sim.context_for_brains import ContextForBrains

from packages.medagogic_sim.gpt.medagogic_gpt import MODEL_GPT4, gpt, UserMessage, SystemMessage, GPTMessage

import logging
from packages.medagogic_sim.logger.logger import get_logger
logger = get_logger(level=logging.DEBUG)


class TaskRunner:
    def __init__(self, npc: MedicalNPC, task: TaskCall):
        self.npc = npc
        self.context = npc.context
        self.task = task

        self.on_dialog = Subject()

        self.pending_tasks: List[asyncio.Task] = []
        self.update_receipt: SimulationUpdateReciept | None = None
        

    async def run(self) -> None:
        action_type: ActionType = ActionType.NONE

        if self.task.type == "connection":
            action_type = ActionType.DEVICE
        elif self.task.type == "intervention":
            action_type = ActionType.INTERVENTION
        elif self.task.type == "assessment":
            action_type = ActionType.ASSESSMENT
        elif self.task.type == "other":
            action_type = ActionType.OTHER
        else:
            raise Exception(f"Unknown task type {self.task.type}")

        # First kickoff the sim update
        if action_type in [ActionType.INTERVENTION, ActionType.PREPARATION]:
            params_str = ", ".join(self.task.call_data.params)
            self.update_receipt = self.context.simulation.applyUpdate(f"{self.npc.definition.name} performed action: `{self.task.call_data.name} ({params_str})`")

            self.update_receipt.on_new_immediate_state_generated.subscribe(self.__handle_current_state_recalculated)
            self.update_receipt.on_finished.subscribe(self.__handle_sim_update_finished)
        else:
            self.add_pending_task(self.__generate_dialog_for_assessment())

        # Then wait for anims and dialog
        anim_task = self.context.animation_resolver.resolve_animation(self.npc.id, self.task.animationId)
        self.add_pending_task(anim_task)
        self.add_pending_task(self.connect_devices_at_right_time())

        # Don't return until we're finished doing, animating, updating, and speaking
        while len(self.pending_tasks) > 0 or self.waiting_for_update():
            self.pending_tasks = [task for task in self.pending_tasks if not task.done()]
            await asyncio.sleep(0.1)

        logger.info(f"TaskRunner finished for {self.task.call_data}")

    def waiting_for_update(self):
        if self.update_receipt:
            return not self.update_receipt.finished
        return False

    def add_pending_task(self, task: Coroutine) -> None:
        self.pending_tasks.append(asyncio.create_task(task))

    async def connect_devices_at_right_time(self):
        await asyncio.sleep(10)

        if self.task.connectDeviceIDs:
            self.npc.context.add_connected_devices(self.task.connectDeviceIDs)


    def __handle_current_state_recalculated(self, data: Tuple[MarkdownExercise, str]) -> None:
        updated_exercise, update_comments = data
        logger.info(f"Current state is updated, now I can calculate dialog...")
        self.add_pending_task(self.__generate_dialog_for_intervention(updated_exercise, update_comments))


    async def __generate_dialog_for_intervention(self, updated_exercise: MarkdownExercise, update_comments: Optional[str]) -> None:
        current_patient_state = self.context.simulation.exercise.current_state.to_markdown()

        sim_results = ""
        if update_comments:
            sim_results = "\n# Simulation Results\n" + update_comments + "\n"

        logger.info(f"Figuring out dialog for intervention: {self.task.call_data} - {update_comments}")

        prompt = f"""
You are {self.npc.markdown_summary()} in a pediatric emergency training simulation.

The user will inform you of an action which you have just completed, along with some information about the new state of the patient and simulation.
What do you say? Max one sentence. Keep your response very brief, and in line with your character and the situation. Be passive rather than active, your response should not guide the user. Compare Initial Patient State and Simulation Results below to observe any consequences of the action..

# Initial Patient State
{current_patient_state}
""".strip()
        
        user_input = f"""
# Your original instruction
{self.task.full_input}

# Completed action
{self.task.call_data.name}

{sim_results}

What do you say? Max one sentence.
""".strip()

        messages: List[GPTMessage] = [
            SystemMessage(prompt),
            UserMessage(user_input)
        ]

        response = await gpt(messages, model=MODEL_GPT4, max_tokens=100, temperature=0)

        logger.info(f"Dialog: {response}")
        self.on_dialog.on_next(response)


    async def __generate_dialog_for_assessment(self) -> None:
        current_patient_state = self.context.simulation.exercise.current_state.to_markdown()

        logger.info(f"Figuring out dialog for assessment: {self.task.call_data}")

        prompt = f"""
You are {self.npc.markdown_summary()} in a pediatric emergency training simulation.

The user will inform you of an action which you have just completed, along with some information about the new state of the patient and simulation.
What do you say? Max one sentence. Keep your response very brief, and in line with your character and the situation. Be passive rather than active, your response should not guide the user. Compare Initial Patient State and Simulation Results below to observe any consequences of the action..

# Current Patient State
{current_patient_state}
""".strip()
        
        user_input = f"""
# Your overall instruction/request
{self.task.full_input}

# The task you need to respond for
{self.task.call_data.name}

What do you say? Max one sentence.
""".strip()

        messages: List[GPTMessage] = [
            SystemMessage(prompt),
            UserMessage(user_input)
        ]

        response = await gpt(messages, model=MODEL_GPT4, max_tokens=100, temperature=0)

        logger.info(f"Dialog: {response}")
        self.on_dialog.on_next(response)


    def __handle_sim_update_finished(self, none: Any) -> None:
        logger.info(f"Oi my update has finished processing!")


if __name__ == "__main__":
    from packages.medagogic_sim.context_for_brains import ContextForBrains
    from packages.medagogic_sim.npc import MedicalNPC
    from packages.medagogic_sim.npc_manager import NPCManager
    logger.setLevel(logging.INFO)

    async def main():
        context = ContextForBrains()
        npc_manager = NPCManager(context)

        npc = list(npc_manager.npcs.values())[0]

        task_runner = TaskRunner(npc, context.action_db.get_action_from_call("Chin lift", "Perform a chin lift please."))

        await task_runner.run()

    asyncio.run(main()) 