from typing import List, Optional

from pydantic import BaseModel, Field
from packages.medagogic_sim.animation_resolver.animation_resolver_base import AnimationResolver_Base
from packages.medagogic_sim.animation_resolver.dummy_animation_resolver import DummyAnimationResolver
from packages.medagogic_sim.exercise.exercise_loader import read_metadata
from packages.medagogic_sim.exercise.simulation4d import LeafyBlossom
from packages.medagogic_sim.action_db.actions_for_brains import ActionDatabase
from packages.medagogic_sim.exercise.simulation_types import BloodPressureModel
from packages.medagogic_sim.history.sim_history import HistoryLog, Evt_Chat_NPCMessage
from packages.medagogic_sim.iomanager import IOManager, NPCSpeech
from packages.medagogic_sim.exercise.devices.device_interface import DeviceInterface
    

class ExposedVitalSigns(BaseModel):
    temperature: Optional[float] = Field(None, description="The body temperature in degrees Celsius or Fahrenheit")
    heart_rate: Optional[float] = Field(None, description="The heart rate in beats per minute")
    respiratory_rate: Optional[float] = Field(None, description="The number of breaths taken per minute")
    blood_pressure: Optional[BloodPressureModel] = Field(None, description="Blood pressure measurements")
    blood_glucose: Optional[float] = Field(None, description="The blood glucose level")
    oxygen_saturation: Optional[float] = Field(None, description="The oxygen saturation in percentage")
    capillary_refill: Optional[float] = Field(None, description="The capillary refill time in seconds")

    def to_markdown(self):
        lines = []
        if self.temperature is not None:
            lines.append(f"- Temperature: {self.temperature:0.1f}°C")
        if self.heart_rate is not None:
            lines.append(f"- Heart Rate: {self.heart_rate:0.0f} bpm")
        if self.respiratory_rate is not None:
            lines.append(f"- Respiratory Rate: {self.respiratory_rate:0.0f} breaths/min")
        if self.blood_pressure is not None:
            lines.append(f"- Blood Pressure: {self.blood_pressure.systolic:0.1f}/{self.blood_pressure.diastolic:0.1f} mmHg")
        if self.blood_glucose is not None:
            lines.append(f"- Blood Glucose: {self.blood_glucose:0.0f} mg/dL")
        if self.oxygen_saturation is not None:
            lines.append(f"- Oxygen Saturation: {self.oxygen_saturation:0.1f}%")
        if self.capillary_refill is not None:
            lines.append(f"- Capillary Refill: {self.capillary_refill:0.0f} seconds")
        
        return "\n".join(lines)
    

class ContextForBrains:
    def __init__(self, exercise_name="pediatric_septic_shock") -> None:
        self.history = HistoryLog()

        self.simulation = LeafyBlossom(exercise_name, self.history)
        self.metadata = read_metadata(exercise_name)
        self.animation_resolver: AnimationResolver_Base = DummyAnimationResolver()
        self.action_db  = ActionDatabase()
        self.iomanager = IOManager()
        self.device_interface = DeviceInterface()

        self.simulation.on_alert.subscribe(self.iomanager.simulation_alert)

        self.iomanager.on_npc_speak.subscribe(self.on_npc_speak)

    def on_npc_speak(self, npc_speech: NPCSpeech):
        self.history.add_event(Evt_Chat_NPCMessage(npc_id=npc_speech.npc_id, content=npc_speech.text))

    def get_exposed_vitals(self) -> ExposedVitalSigns:
        vital_signs = self.simulation.getCurrentVitals()
        exposed_vital_types = self.device_interface.exposed_vitals()
        as_dict = vital_signs.model_dump()

        exposed_dict = {}
        for vital_type in exposed_vital_types:
            if vital_type in as_dict:
                exposed_dict[str(vital_type)] = as_dict[vital_type]

        return ExposedVitalSigns(**exposed_dict)