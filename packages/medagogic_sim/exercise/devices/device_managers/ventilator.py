from packages.medagogic_sim.action_db.actions_for_brains import ActionModel
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
    
    @staticmethod
    def get_action_model() -> ActionModel:
        example_data = [
            ActionExample(input="Connect ventilator in AC mode with fio2 0.5", 
                        action="Connect ventilator (AC, 0.5)"),
            ActionExample(input="Ventilator to PC mode and 0.7 fio2", 
                        action="Connect ventilator (PC, 0.7)"),
            ActionExample(input="Switch to PSV and set fio2 to 0.3", 
                        action="Connect ventilator (PSV, 0.3)")
        ]

        return ActionModel(
            name="Connect ventilator ($mode, $fio2)",
            description="Connect to a ventilator with specified mode and fio2 settings.",
            exampleInputs=["Connect ventilator in AC mode", "Switch to PC mode, fio2 0.7", "Set ventilator to PSV mode with 0.3 fio2"],
            examples=example_data,
            requirements=[],
            animationId="connect ventilator",
            type="connection"
        )