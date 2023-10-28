from typing import Optional
from pydantic import BaseModel, Field
from packages.medagogic_sim.context_for_brains import ContextForBrains
from packages.medagogic_sim.dialog_router import TeamLeadDialog
from packages.medagogic_sim.exercise.simulation_types import BloodPressureModel, VitalSigns
from packages.medagogic_sim.history import sim_history
import asyncio

from packages.medagogic_sim.npc_manager import NPCManager


class ExposedVitalSigns(BaseModel):
    temperature: Optional[float] = Field(None, description="The body temperature in degrees Celsius or Fahrenheit")
    heart_rate: Optional[float] = Field(None, description="The heart rate in beats per minute")
    respiratory_rate: Optional[float] = Field(None, description="The number of breaths taken per minute")
    blood_pressure: Optional[BloodPressureModel] = Field(None, description="Blood pressure measurements")
    blood_glucose: Optional[float] = Field(None, description="The blood glucose level")
    oxygen_saturation: Optional[float] = Field(None, description="The oxygen saturation in percentage")
    capillary_refill: Optional[float] = Field(None, description="The capillary refill time in seconds")

class MedagogicSimulator:
    def __init__(self, exercise_name: str="pediatric_septic_shock"):
        self.exercise_name = exercise_name
        self.context = ContextForBrains(exercise_name)
        self.npc_manager = NPCManager(self.context)

    async def process_user_input(self, input_text: str, to_npc_id: Optional[str]=None) -> None:
        self.context.history.add_event(sim_history.Evt_ChatMessage(name="Team Lead", content=input_text))

        if to_npc_id and to_npc_id in self.npc_manager.npcs:
            npc = self.npc_manager.npcs[to_npc_id]
            await npc.process_input(input_text)
        else:
            await self.npc_manager.process_dialog(TeamLeadDialog(input_text))

    def get_exposed_vitals(self) -> ExposedVitalSigns:
        vital_signs = self.context.simulation.getCurrentVitals()
        exposed_vital_types = self.context.device_interface.exposed_vitals()
        as_dict = vital_signs.model_dump()

        exposed_dict = {}
        for vital_type in exposed_vital_types:
            if vital_type in as_dict:
                exposed_dict[vital_type] = as_dict[vital_type]

        return ExposedVitalSigns(**exposed_dict)

if __name__ == "__main__":
    import logging
    from packages.medagogic_sim.npc import logger as npc_logger

    npc_logger.setLevel(logging.DEBUG)

    async def main():
        simulator = MedagogicSimulator()

        simulator.context.device_interface.nibp_manager.connect({})

        print(simulator.get_exposed_vitals())

        # await simulator.process_user_input("Get IV access")

        # while True:
        #     await asyncio.sleep(1)

    asyncio.run(main())