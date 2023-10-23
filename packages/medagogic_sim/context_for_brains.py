from typing import List
from packages.medagogic_sim.animation_resolver.animation_resolver_base import AnimationResolver_Base
from packages.medagogic_sim.animation_resolver.dummy_animation_resolver import DummyAnimationResolver
from packages.medagogic_sim.exercise.device_definitions import DeviceConfig
from packages.medagogic_sim.exercise.exercise_loader import read_metadata
from packages.medagogic_sim.exercise.simulation4d import LeafyBlossom
from packages.medagogic_sim.actions_for_brains import ActionDatabase
from packages.medagogic_sim.history.sim_history import HistoryLog
from packages.medagogic_sim.iomanager import IOManager

    

class ContextForBrains:
    def __init__(self, exercise_name="pediatric_septic_shock") -> None:
        self.history = HistoryLog()

        self.simulation = LeafyBlossom(exercise_name, self.history)
        self.metadata = read_metadata(exercise_name)
        self.animation_resolver: AnimationResolver_Base = DummyAnimationResolver()
        self.action_db  = ActionDatabase()
        self.iomanager = IOManager()

        self.simulation.on_alert.subscribe(self.iomanager.simulation_alert)

    # TODO: All of this
    @property
    def connected_device_ids(self) -> List[DeviceConfig]:
        return []
    
    @property
    def interventions_markdown(self) -> str:
        return ""

    def add_connected_devices(self, device_ids: List[str]) -> None:
        pass