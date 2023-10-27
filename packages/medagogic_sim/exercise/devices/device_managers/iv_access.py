from .default_device_imports import *
logger = get_logger(level=logging.WARNING)



class IVAccessLocation(str, Enum):
    LEFT_HAND = "left hand"
    RIGHT_HAND = "right hand"

class IVAccessParams(BaseModel):
    location: IVAccessLocation


class IVAccessManager(DeviceHandler_Base):
    def __init__(self) -> None:
        self.connected_ivs: Dict[IVAccessLocation, IVAccessParams] = {}

        self.action_name = "Obtain IV access"
        self.default_params = IVAccessParams(location=IVAccessLocation.LEFT_HAND)

    def handle_call(self, call_data: ActionDatabase.CallData) -> str:
        return self.connect(self.default_params)

    def connect(self, params: IVAccessParams) -> str:
        if params.location in self.connected_ivs:
            raise Exception(f"IV already connected to {params.location}")
        self.connected_ivs[params.location] = params
        return f"IV access established in {params.location.value}"

    @staticmethod
    def connection_params_markdown() -> List[str]:
        return IVAccessManager._params_to_md(IVAccessParams)
    
    def get_state(self) -> str:
        if not self.is_connected:
            return "No IV access"
        else:
            output = "IV access established in " + ", ".join([f"{loc.value}" for loc in self.connected_ivs.keys()])
            return output
        
    @property
    def is_connected(self) -> bool:
        return len(self.connected_ivs) > 0