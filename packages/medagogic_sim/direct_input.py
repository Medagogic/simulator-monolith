

import asyncio
from typing import List
from packages.medagogic_sim.action_db.actions_for_brains import TaskCall
from packages.medagogic_sim.context_for_brains import ContextForBrains
from packages.medagogic_sim.npcs.direct_task_runner import DirectTaskRunner
from packages.medagogic_sim.npcs.the_brains import NPCBrain

import logging
from packages.medagogic_sim.logger.logger import get_logger
logger = get_logger(level=logging.INFO)


class DirectInput:
    def __init__(self, context: ContextForBrains):
        self.context = context
        self.id = "Sam"
        
        self.brain = NPCBrain(self.context, self)
        self.brain.on_dialog.subscribe(self.__handle_brain_dialog)
        self.brain.on_actions.subscribe(self.__handle_brain_actions)
        self.brain.on_error.subscribe(self.__handle_brain_error)
        
        self.task_queue: List[TaskCall] = []

    def __handle_brain_dialog(self, dialog: str) -> None:
        self.context.iomanager.npc_speak(self.id, "Sam", dialog)

    def __handle_brain_actions(self, actions: List[TaskCall]) -> None:
        logger.debug(f"New actions: {[action.call_data for action in actions]}")
        async def run_actions():
            for action in actions:
                await self.perform_task(action)
        asyncio.create_task(run_actions())

    def __handle_brain_error(self, error: str) -> None:
        logger.error(f"Brain error: {error}")

    async def process_input(self, user_input: str) -> None:
        try:
            await self.brain.process_user_input(user_input)
        except Exception as e:
            logger.error(e)
            raise e

    async def perform_task(self, task: TaskCall):
        current_task_runner = DirectTaskRunner(self.context, task)
        current_task_runner.on_dialog.subscribe(self.__handle_brain_dialog)
        await current_task_runner.run()

    def markdown_summary(self):
        return ""