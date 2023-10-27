from packages.medagogic_sim.exercise.devices.device_managers.default_device_imports import *
logger = get_logger(level=logging.WARNING)


class NIBPMonitorParams(BaseModel):
    pass

class NIBPMonitor(DeviceHandler_Base):
    def __init__(self) -> None:
        self.nibp_params: Optional[NIBPMonitorParams] = None
        self.action_name = "Connect BP monitor"

    def handle_call(self, call_data: ActionDatabase.CallData) -> str:
        return self.connect(NIBPMonitorParams())

    def connect(self, params: NIBPMonitorParams):
        if self.is_connected:
            raise Exception("NIBP already connected")
        self.nibp_params = params
        return "NIBP monitor connected"

    @staticmethod
    def connection_params_markdown() -> List[str]:
        return NIBPMonitor._params_to_md(NIBPMonitorParams)

    def get_state(self) -> str:
        if not self.is_connected:
            return "NIBP monitor not connected"
        else:
            return f"NIBP monitor connected"

    def exposed_vitals(self) -> List[Vitals]:
        if not self.is_connected:
            return []
        return [Vitals.BLOOD_PRESSURE]
    
    @property
    def is_connected(self) -> bool:
        return self.nibp_params is not None