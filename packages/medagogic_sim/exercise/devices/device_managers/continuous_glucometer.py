from packages.medagogic_sim.exercise.devices.device_managers.default_device_imports import *
logger = get_logger(level=logging.WARNING)


class ContinuousGlucometerParams(BaseModel):
    pass

class ContinuousGlucometer(DeviceHandler_Base):
    def __init__(self) -> None:
        self.connection_params: Optional[ContinuousGlucometerParams] = None

    def handle_call(self, call_data: ActionDatabase.CallData) -> str:
        return self.connect(ContinuousGlucometerParams())

    def connect(self, params: ContinuousGlucometerParams):
        if self.is_connected:
            raise Exception("Continuous Glucometer already connected")
        self.connection_params = params
        return f"Continuous Glucometer connected"

    @staticmethod
    def connection_params_markdown() -> List[str]:
        return ContinuousGlucometer._params_to_md(ContinuousGlucometerParams)
    
    def get_state(self) -> str:
        if not self.is_connected:
            return "Continuous Glucometer not connected"
        else:
            return f"Continuous Glucometer connected"
        
    def exposes_vitals(self) -> List[Vitals]:
        return [Vitals.BLOOD_GLUCOSE]
    
    @property
    def is_connected(self) -> bool:
        return self.connection_params is not None