import asyncio
from typing import List, Optional

from pydantic import BaseModel, Field
from packages.medagogic_sim.animation_resolver.animation_resolver_base import AnimationResolver_Base
from packages.medagogic_sim.animation_resolver.dummy_animation_resolver import DummyAnimationResolver
from packages.medagogic_sim.exercise.markdownexercise import MarkdownExercise
from packages.medagogic_sim.exercise.metadata_loader import ExerciseMetadata
# from packages.medagogic_sim.exercise.exercise_loader import read_metadata
from packages.medagogic_sim.exercise.simulation4d import LeafyBlossom
from packages.medagogic_sim.action_db.actions_for_brains import ActionDatabase
from packages.medagogic_sim.exercise.simulation_types import BloodPressureModel
from packages.medagogic_sim.exercise_storage.exercise_storage import ExerciseStorage
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

        storage = ExerciseStorage()
        self.exercise_data = storage.LoadExercise(exercise_name)
        self.metadata = ExerciseMetadata.from_markdown_str(self.exercise_data.exerciseMetadata)

        markdown_exercise = MarkdownExercise.from_markdown(self.exercise_data.exerciseData)
        self.simulation = LeafyBlossom(markdown_exercise, self.history)
        
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
            vital_key = vital_type.value
            if vital_type in as_dict:
                exposed_dict[vital_key] = as_dict[vital_key]

        return ExposedVitalSigns(**exposed_dict)
    

if __name__ == "__main__":
    async def main():
        context = ContextForBrains()
        print(context.get_exposed_vitals())

    asyncio.run(main())