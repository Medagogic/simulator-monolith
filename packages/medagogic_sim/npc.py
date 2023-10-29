from __future__ import annotations
import asyncio
from typing import List, TYPE_CHECKING, Optional

from packages.medagogic_sim.npc_actions import BraniacActioner
from packages.medagogic_sim.npc_definitions import NPCDefinition
from packages.medagogic_sim.the_brains import NPCBrain
from packages.medagogic_sim.action_db.actions_for_brains import TaskCall

if TYPE_CHECKING:
    from packages.medagogic_sim.context_for_brains import ContextForBrains

import logging
from packages.medagogic_sim.logger.logger import get_logger
logger = get_logger(level=logging.INFO)


def get_test_npc(context: ContextForBrains) -> MedicalNPC:
    npc = MedicalNPC(context, definition=NPCDefinition(
        name="Dr. Tester",
        role="Senior Resident",
        specialities=["Emergency Medicine", "Critical Care"],
        years_of_experience=5
    ), id="dr_tester")

    return npc

# NPCs do not emit IO events/subjects, they call into the IO manager

class MedicalNPC():
    def __init__(self, context: ContextForBrains, definition: NPCDefinition, id: str):
        self.context = context
        self.definition = definition
        self.id = id
        
        self.brain = NPCBrain(self.context, self)
        self.brain.on_dialog.subscribe(self.__handle_brain_dialog)
        self.brain.on_actions.subscribe(self.__handle_brain_actions)
        self.brain.on_error.subscribe(self.__handle_brain_error)

        self.actioner = BraniacActioner(self)

        self.actioner.on_dialog.subscribe(self.__handle_brain_dialog)

        self.task_queue: List[TaskCall] = []
        
    def __handle_brain_dialog(self, dialog: str) -> None:
        self.context.iomanager.npc_speak(self.id, self.definition.name, dialog)

    def __handle_brain_actions(self, actions: List[TaskCall]) -> None:
        logger.debug(f"New actions: {[action.call_data for action in actions]}")
        self.add_actions(actions)

    def __handle_brain_error(self, error: str) -> None:
        self.context.iomanager.npc_speak(self.id, self.definition.name, f"Right brain found a problem: {error}")

    def add_actions(self, actions):
        self.task_queue += actions
        self.__try_start_next_task()

    def __try_start_next_task(self):
        if not self.actioner.current_task and len(self.task_queue) > 0:
            task_to_start = self.task_queue[0]
            self.task_queue = self.task_queue[1:]
            asyncio.create_task(self.perform_task(task_to_start))

    async def perform_task(self, task: TaskCall) -> None:
        logger.info(f"Performing task: {task.call_data}")
        self.context.iomanager.npc_start_action(self.id, self.definition.name, task)
        await self.actioner.perform_task(task)
        self.context.iomanager.npc_finished_action(self.id, self.definition.name, task)
        self.__try_start_next_task()

    async def process_input(self, user_input: str) -> None:
        self.context.iomanager.npc_start_thinking(self.id, self.definition.name, user_input)
        try:
            await self.brain.process_user_input(user_input)
        except Exception as e:
            logger.error(e)
            self.context.iomanager.npc_stop_thinking(self.id, self.definition.name)
            raise e
        self.context.iomanager.npc_stop_thinking(self.id, self.definition.name)


    def markdown_summary(self) -> str:
        name = self.definition.name
        action: str | None = self.actioner.current_task_description
        specialities = self.definition.specialities
        years_of_experience = self.definition.years_of_experience

        npc_line = f"- {name}"

        npc_line += f"\n\t- Years of experience: {years_of_experience}"

        specialities_line = "\n\t- Specialties: "
        for specialty in specialities:
            specialities_line += f"{specialty}, "
        if specialities_line.endswith(", "):
            specialities_line = specialities_line[:-2]
        npc_line += specialities_line

        if action is not None:
            npc_line += f"\n\t- Busy - {action}"
        else:
            npc_line += "\n\t- Currently idle"

        return npc_line


    
if __name__ == "__main__":
    from packages.medagogic_sim.context_for_brains import ContextForBrains
    from packages.medagogic_sim.npc_manager import NPCManager

    logger.setLevel(logging.DEBUG)

    async def main():
        context = ContextForBrains()
        npc_manager = NPCManager(context)

        npc = list(npc_manager.npcs.values())[0]

        await npc.process_input("check the airway and perform a chin lift if needed")

        while True:
            await asyncio.sleep(1)

    asyncio.run(main())