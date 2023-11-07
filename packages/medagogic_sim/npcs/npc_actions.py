from __future__ import annotations
import asyncio
from pydantic import BaseModel
import typing

from packages.medagogic_sim.exercise.simulation_types import ActionType
from packages.medagogic_sim.action_db.actions_for_brains import TaskCall
from packages.medagogic_sim.npcs.npc_task_runner import TaskRunner


if typing.TYPE_CHECKING:
    from packages.medagogic_sim.npcs.npc import MedicalNPC
    

from rx.subject import Subject

import logging
from packages.medagogic_sim.logger.logger import get_logger
logger = get_logger(level=logging.DEBUG)


class NPCStaticData(BaseModel):
    id: str
    name: str
    specialities: str
    yearsExperience: str

class BraniacActioner:
    def __init__(self, npc: MedicalNPC):
        self.npc = npc

        self.current_task_runner: TaskRunner | None = None

        self.on_action_complete = Subject()
        self.on_dialog = Subject()


    @property
    def current_task(self) -> TaskCall | None:
        if self.current_task_runner:
            return self.current_task_runner.task
        return None


    @property
    def current_task_description(self) -> str | None:
        if self.current_task:
            return self.current_task.description
        return None

    async def perform_task(self, task: TaskCall):
        if self.current_task:
            raise Exception("Already performing an action")
        
        self.current_task_runner = TaskRunner(self.npc, task)

        self.current_task_runner.on_dialog.subscribe(self.__handle_task_runner_dialog)
    
        await self.current_task_runner.run()
            
        self.on_action_complete.on_next(task)
        self.current_task_runner = None


    def __handle_task_runner_dialog(self, dialog: str) -> None:
        self.on_dialog.on_next(dialog)


if __name__ == "__main__":
    from packages.medagogic_sim.context_for_brains import ContextForBrains
    from packages.medagogic_sim.npcs.npc import MedicalNPC
    logger.setLevel(logging.DEBUG)

    async def main():
        context = ContextForBrains()

        npc = MedicalNPC(context)

        action_0 = context.action_db.get_action_from_call("Assess airway")
        action_1 = context.action_db.get_action_from_call("Chin lift")

        npc.add_actions([action_0, action_1])

        while True:
            await asyncio.sleep(1)

    asyncio.run(main())