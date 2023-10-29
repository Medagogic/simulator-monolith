from packages.medagogic_sim.action_db.actions_for_brains import ActionModel
from .default_device_imports import *
logger = get_logger(level=logging.WARNING)


class EKGConnectionParams(BaseModel):
    pass

class EKGConnection(DeviceHandler_Base):
    def __init__(self) -> None:
        self.ekg_connected: bool = False
        self.action_name = "Connect EKG/ECG"

    def handle_call(self, call_data: ActionDatabase.CallData) -> str:
        return self.connect(EKGConnectionParams())

    def connect(self, params: EKGConnectionParams) -> str:
        if self.ekg_connected:
            raise Exception(f"EKG already connected")
        self.ekg_connected = True
        return f"EKG connected"

    @staticmethod
    def connection_params_markdown() -> List[str]:
        return EKGConnection._params_to_md(EKGConnectionParams)
    
    def get_state(self) -> str:
        if not self.is_connected:
            return "EKG not connected"
        else:
            return "EKG connected"
        
    def exposed_vitals(self) -> List[Vitals]:
        if not self.is_connected:
            return []
        return [Vitals.HEART_RATE, Vitals.RESPIRATORY_RATE]
    
    @property
    def is_connected(self) -> bool:
        return self.ekg_connected
    
    @staticmethod
    def get_action_model() -> ActionModel:
        return ActionModel(
            name="Connect EKG/ECG",
            description="Attach electrocardiogram leads to the patient to monitor the heart's electrical activity",
            exampleInputs=["Get the EKG connected", "Connect a 12-lead EKG", "Connect a 3-lead EKG"],
            examples=["Get the EKG connected", "Connect a 12-lead EKG", "Connect a 3-lead EKG"],
            requirements=[],
            animationId="connect ekg",
            type="connection"
        )