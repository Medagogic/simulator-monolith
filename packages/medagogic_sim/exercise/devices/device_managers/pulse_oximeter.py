from packages.medagogic_sim.exercise.devices.device_managers.default_device_imports import *
logger = get_logger(level=logging.WARNING)


class PulseOximeterParams(BaseModel):
    probe_position: str = Field(..., description='Type of probe used, e.g., "Finger", "Earlobe", "Foot"')

class PulseOximeter(DeviceHandler_Base):
    def __init__(self) -> None:
        self.connection_params: Optional[PulseOximeterParams] = None
        self.action_name = "Connect pulse oximeter"
        self.default_params = PulseOximeterParams(probe_position="Finger")

    def extract_params(self, call_data: ActionDatabase.CallData) -> PulseOximeterParams:
        params = PulseOximeterParams(**self.default_params.model_dump())
        if len(call_data.params) > 0:
            params.probe_position = call_data.params[0]

        return params

    def handle_call(self, call_data: ActionDatabase.CallData) -> str:
        return self.connect(self.extract_params(call_data))

    def connect(self, params: PulseOximeterParams):
        if self.is_connected:
            raise Exception("Pulse Oximeter already connected")
        self.connection_params = params
        return f"Pulse Oximeter connected on {params.probe_position}"

    @staticmethod
    def connection_params_markdown() -> List[str]:
        return PulseOximeter._params_to_md(PulseOximeterParams)

    def get_state(self) -> str:
        if not self.is_connected:
            return "Pulse Oximeter not connected"
        else:
            return f"Pulse Oximeter connected on {self.connection_params.probe_position}"   # type: ignore

    def exposed_vitals(self) -> List[Vitals]:
        if not self.is_connected:
            return []
        return [Vitals.HEART_RATE, Vitals.OXYGEN_SATURATION]
    
    @property
    def is_connected(self) -> bool:
        return self.connection_params is not None