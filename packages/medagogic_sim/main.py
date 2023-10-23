from packages.medagogic_sim.context_for_brains import ContextForBrains
from packages.medagogic_sim.dialog_router import TeamLeadDialog
from packages.medagogic_sim.exercise.simulation_types import VitalSigns
from packages.medagogic_sim.npc import logger as npc_logger
import logging
import asyncio

from packages.medagogic_sim.npc_manager import NPCManager

class MedagogicSimulator:
    def __init__(self, exercise_name: str="pediatric_septic_shock"):
        self.exercise_name = exercise_name
        self.context = ContextForBrains(exercise_name)
        self.npc_manager = NPCManager(self.context)

    async def process_user_input(self, input_text: str) -> None:
        await self.npc_manager.process_dialog(TeamLeadDialog(input_text))

    def get_vitals(self) -> VitalSigns:
        return self.context.simulation.getCurrentVitals()

if __name__ == "__main__":
    npc_logger.setLevel(logging.DEBUG)

    async def main():
        simulator = MedagogicSimulator()
        await simulator.process_user_input("Hello team")

        while True:
            await asyncio.sleep(1)

    asyncio.run(main())