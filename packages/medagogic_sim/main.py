from typing import Optional
from pydantic import BaseModel, Field
from packages.medagogic_sim.context_for_brains import ContextForBrains
from packages.medagogic_sim.dialog_router import TeamLeadDialog
from packages.medagogic_sim.direct_input import DirectInput
from packages.medagogic_sim.dr_clippy import DrClippy
from packages.medagogic_sim.exercise.simulation_types import BloodPressureModel, VitalSigns
from packages.medagogic_sim.history import sim_history
import asyncio
from packages.medagogic_sim.learner_actions.learner_action_evaluator import LearnerActionEvaluator

from packages.medagogic_sim.npcs.npc_manager import NPCManager




class MedagogicSimulator:
    def __init__(self, exercise_name: str="pediatric_septic_shock"):
        self.exercise_name = exercise_name
        self.context = ContextForBrains(exercise_name)
        self.npc_manager = NPCManager(self.context)
        self.dr_clippy = DrClippy(self.context)
        self.direct_input = DirectInput(self.context)
        self.learner_action_evaluator = LearnerActionEvaluator(self.context)

        self.context.history.add_event(sim_history.Evt_Chat_Event(content="Welcome to the Medagogic Simulator!"))


    async def process_user_input(self, input_text: str, to_npc_id: Optional[str]=None) -> None:
        self.context.history.add_event(sim_history.Evt_Chat_HumanMessage(content=input_text))
        await self.direct_input.process_input(input_text)


    # async def process_user_input(self, input_text: str, to_npc_id: Optional[str]=None) -> None:
    #     self.context.history.add_event(sim_history.Evt_Chat_HumanMessage(content=input_text))

    #     if to_npc_id and to_npc_id in self.npc_manager.npcs:
    #         npc = self.npc_manager.npcs[to_npc_id]
    #         await npc.process_input(input_text)
    #     else:
    #         await self.npc_manager.process_dialog(TeamLeadDialog(input_text))

if __name__ == "__main__":
    import logging
    from packages.medagogic_sim.npcs.npc import logger as npc_logger

    npc_logger.setLevel(logging.DEBUG)

    async def main():
        simulator = MedagogicSimulator()

        # simulator.context.device_interface.nibp_manager.connect({})

        await simulator.process_user_input("Get IV access and connect the ECG")

        while True:
            await asyncio.sleep(1)

    asyncio.run(main())