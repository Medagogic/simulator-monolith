from typing import Final, List, Optional
from pydantic import BaseModel
from packages.medagogic_sim.exercise.simulation_types import ActionType, Vitals

class DeviceConfig(BaseModel):
    display_name: str
    reveals: List[Vitals]
    animation_id: str
    resolution_instructions: Optional[str] = None

    @property
    def id(self) -> str:
        return self.display_name.lower() #.replace(" ", "_")
    
    @property
    def action_type(self) -> ActionType:
        return ActionType.DEVICE

DEVICE_CONFIG: Final[List[DeviceConfig]] = [
    DeviceConfig(display_name="EKG", reveals=[Vitals.HEART_RATE, Vitals.RESPIRATORY_RATE], animation_id="connect ekg"),
    DeviceConfig(display_name="Pulse Oximeter", reveals=[Vitals.OXYGEN_SATURATION, Vitals.HEART_RATE], animation_id="connect blood pressure cuff"),
    DeviceConfig(display_name="Blood Pressure Monitor", reveals=[Vitals.BLOOD_PRESSURE], animation_id="connect blood pressure cuff"),
    DeviceConfig(display_name="Temperature Probe", reveals=[Vitals.TEMPERATURE], animation_id="inspect limbs"),
    DeviceConfig(display_name="IV Access", reveals=[], animation_id="establish IV access"),
    DeviceConfig(display_name="IO Access", reveals=[], animation_id="establish IO access"),
]
