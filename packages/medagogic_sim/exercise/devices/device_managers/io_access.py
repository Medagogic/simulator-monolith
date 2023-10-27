from packages.medagogic_sim.exercise.devices.device_managers.default_device_imports import *

logger = get_logger(level=logging.WARNING)


class IOAccessLocation(Enum):
    PROXIMAL_TIBIA = "proximal tibia"
    DISTAL_TIBIA = "distal tibia"
    DISTAL_FEMUR = "distal femur"

class IOBodySide(Enum):
    LEFT = "left"
    RIGHT = "right"


class IOAccessParams(BaseModel):
    location: IOAccessLocation
    needle_size: str = Field(default=None, pattern=r'\d+G', description='Gauge of needle, eg "18G", "20G", "22G"')
    side: IOBodySide = Field(default=None, description='Side of body, e.g., "left", "right"')


class IOAccessManager(DeviceHandler_Base):
    def __init__(self) -> None:
        self.connected_ios: Dict[IOAccessLocation, IOAccessParams] = {}
        self.action_name = "Obtain IO access ($location, $size)"
        self.default_params = IOAccessParams(location=IOAccessLocation.PROXIMAL_TIBIA, needle_size="18G", side=IOBodySide.LEFT)


    def extract_params(self, call_data: ActionDatabase.CallData) -> IOAccessParams:
        params = IOAccessParams(**self.default_params.model_dump())

        for p in call_data.params:
            matched_location = FuzzyEnumMatcher.str_to_enum(p.strip(), IOAccessLocation)
            if matched_location:
                params.location = matched_location
            elif re.match(r'\d+G', p.strip()):
                params.needle_size = p.strip()
            else:
                raise Exception(f"Invalid parameters for {self.action_name}: {call_data.params}")

        return params
    

    def handle_call(self, call_data: ActionDatabase.CallData) -> str:
        return self.connect(self.extract_params(call_data))


    def connect(self, params: IOAccessParams):
        if params.location in self.connected_ios:
            raise Exception(f"IO already connected to {params.location}")
        self.connected_ios[params.location] = params
        return self.connection_str(params)
    
    def connection_str(self, params: IOAccessParams):
        return f"IO access established in {params.side.value} {params.location.value} ({params.needle_size})"

    @staticmethod
    def connection_params_markdown() -> List[str]:
        return IOAccessManager._params_to_md(IOAccessParams)
    
    def get_state(self) -> str:
        if not self.is_connected:
            return "No IO access"
        else:
            output = ""
            for connected_io in self.connected_ios.values():
                output += self.connection_str(connected_io) + "\n"
            return output.strip()
        
    @property
    def is_connected(self) -> bool:
        return len(self.connected_ios) > 0