from packages.medagogic_sim.exercise.devices.device_managers.default_device_imports import *
logger = get_logger(level=logging.WARNING)


class VentilatorParams(BaseModel):
    mode: str = Field(..., description='Ventilation mode, e.g., "AC", "PC", "PSV"')
    fio2: float = Field(..., description='Fraction of Inspired Oxygen, a value between 0.21 and 1.0')

class Ventilator(DeviceHandler_Base):
    def __init__(self) -> None:
        self.connection_params: Optional[VentilatorParams] = None

    def handle_call(self, call_data: ActionDatabase.CallData) -> str:
        return self.connect(VentilatorParams(mode=call_data.params[0], fio2=float(call_data.params[1])))

    def connect(self, params: VentilatorParams):
        if self.is_connected:
            raise Exception("Ventilator already connected")
        self.connection_params = params
        return f"Ventilator connected in {params.mode} mode, FiO2: {params.fio2}"

    @staticmethod
    def connection_params_markdown() -> List[str]:
        return Ventilator._params_to_md(VentilatorParams)

    def get_state(self) -> str:
        if not self.is_connected:
            return "Ventilator not connected"
        else:
            return f"Ventilator connected in {self.connection_params.mode} mode, FiO2: {self.connection_params.fio2}"   # type: ignore

    def exposed_vitals(self) -> List[Vitals]:
        if not self.is_connected:
            return []
        return [Vitals.RESPIRATORY_RATE] # [Vitals.CO2_LEVEL]
    
    @property
    def is_connected(self) -> bool:
        return self.connection_params is not None