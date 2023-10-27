from typing import List
from packages.medagogic_sim.animation_resolver.animation_resolver_base import AnimationResolver_Base
from packages.medagogic_sim.animation_resolver.dummy_animation_resolver import DummyAnimationResolver
from packages.medagogic_sim.exercise.exercise_loader import read_metadata
from packages.medagogic_sim.exercise.simulation4d import LeafyBlossom
from packages.medagogic_sim.actions_for_brains import ActionDatabase
from packages.medagogic_sim.history.sim_history import Evt_ChatMessage, HistoryLog
from packages.medagogic_sim.iomanager import IOManager, NPCSpeech
from packages.medagogic_sim.exercise.devices.device_interface import DeviceInterface
    

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
        self.history.add_event(Evt_ChatMessage(name=npc_speech.npc_name, content=npc_speech.text))

    # TODO: All of this
    @property
    def interventions_markdown(self) -> str:
        return ""
