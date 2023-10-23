from __future__ import annotations
import asyncio
from typing import List, TYPE_CHECKING

from packages.medagogic_sim.npc_actions import BraniacActioner
from packages.medagogic_sim.npc_definitions import NPCDefinition
from packages.medagogic_sim.the_brains import NPCBrain
from packages.medagogic_sim.actions_for_brains import TaskCall

if TYPE_CHECKING:
    from packages.medagogic_sim.context_for_brains import ContextForBrains

import logging
from packages.medagogic_sim.logger.logger import get_logger
logger = get_logger(level=logging.DEBUG)



class MedicalNPC():
    def __init__(self, context: ContextForBrains, definition: NPCDefinition, id: str):
        self.context = context
        self.definition = definition
        self.id = id
        
        self.brain = NPCBrain(self.context)
        self.brain.on_dialog.subscribe(self.__handle_brain_dialog)
        self.brain.on_actions.subscribe(self.__handle_brain_actions)
        self.brain.on_error.subscribe(self.__handle_brain_error)

        self.actioner = BraniacActioner(self)

        self.actioner.on_dialog.subscribe(self.__handle_brain_dialog)

        self.task_queue: List[TaskCall] = []
        
    def __handle_brain_dialog(self, dialog: str) -> None:
        self.context.iomanager.npc_speak(self.id, self.definition.name, dialog)

    def __handle_brain_actions(self, actions: List[TaskCall]) -> None:
        logger.info(f"New actions: {actions}")
        self.add_actions(actions)

    def __handle_brain_error(self, error: str) -> None:
        self.context.iomanager.npc_speak(self.id, self.definition.name, error)

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
        await self.actioner.perform_task(task)
        self.__try_start_next_task()

    async def process_input(self, user_input: str) -> None:
        await self.brain.process_user_input(user_input)

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

    logger.setLevel(logging.DEBUG)

    async def main():
        context = ContextForBrains()

        npc = MedicalNPC(context)

        await npc.process_input("check the airway and perform a chin lift if needed")

        while True:
            await asyncio.sleep(1)

    asyncio.run(main())