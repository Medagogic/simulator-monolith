from __future__ import annotations
from enum import Enum

from typing import Any, Dict, Final, Generic, List, Optional, Type, TypeVar
from pydantic import BaseModel, Field
from packages.medagogic_sim.exercise.simulation_types import ActionType, Vitals
from packages.medagogic_sim.actions_for_brains import ActionDatabase, ActionModel, TaskCall, loadActions
import asyncio
import json
import jsonschema2md


from packages.medagogic_sim.logger.logger import get_logger, logging

logger = get_logger(level=logging.DEBUG)


from difflib import SequenceMatcher
T = TypeVar("T", bound=Enum)
V = TypeVar("V")
class FuzzyEnumMatcher(Generic[T, V]):
    @staticmethod
    def str_to_enum(input_str: str, enum_cls: Type[T]) -> Optional[T]:
        best_match = None
        best_ratio = 0.0

        for enum_item in enum_cls:
            ratio = SequenceMatcher(None, input_str, str(enum_item.value)).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_match = enum_item

        return best_match if best_ratio > 0.9 else None

class DeviceConnectionManager_Base:
    action_name: str = "NOT SET"

    @staticmethod
    def connection_params_markdown() -> List[str]:
        return []
    
    def get_state(self) -> str:
        return ""
    
    def exposed_vitals(self) -> List[Vitals]:
        return []
    
    def handle_call(self, call_data: ActionDatabase.CallData) -> str:
        print(call_data)
        pass
    
    @staticmethod
    def __inline_schema_refs(schema: Dict):
        def _lookup(ref: str):
            ref = ref.replace("#/$defs/", "")
            return schema["$defs"][ref]
        
        def _inline_refs_recursive(schema_part: Any):
            if isinstance(schema_part, dict):
                if "$ref" in schema_part:
                    resolved = _lookup(schema_part["$ref"])
                    schema_part = resolved
                else:
                    for k, v in schema_part.items():
                        schema_part[k] = _inline_refs_recursive(v)
            elif isinstance(schema_part, list):
                for i, item in enumerate(schema_part):
                    schema_part = _inline_refs_recursive(item)
            
            return schema_part


        resolved_schema = {}

        for id, obj in schema["properties"].items():
            resolved_schema[id] = _inline_refs_recursive(obj)

        return resolved_schema

    @staticmethod
    def _params_to_md(params_type: Type[BaseModel]) -> List[str]:
        schema = params_type.model_json_schema()
        schema = DeviceConnectionManager_Base.__inline_schema_refs(schema)
        parser = jsonschema2md.Parser()
        md_lines = parser.parse_schema({"properties": schema})
        md_lines = [l.strip() for l in md_lines if l.strip() != ""]
        params = md_lines[2:]
        
        return params


class IVAccessLocation(Enum):
    LEFT_HAND = "left hand"
    RIGHT_HAND = "right hand"

class IVAccessParams(BaseModel):
    location: IVAccessLocation


class IVAccessManager(DeviceConnectionManager_Base):
    def __init__(self) -> None:
        self.connected_ivs: Dict[IVAccessLocation, IVAccessParams] = {}

        self.action_name = "Obtain IV access ($location)"

    def handle_call(self, call_data: ActionDatabase.CallData) -> str:
        params = call_data.params
        location_str = params[0].strip()
        location_enum = FuzzyEnumMatcher.str_to_enum(location_str, IVAccessLocation)
        if location_enum:
            return self.connect(IVAccessParams(location=location_enum))
        
        raise Exception(f"Invalid parameters for {self.action_name}: {params}")

    def connect(self, params: IVAccessParams) -> str:
        if params.location in self.connected_ivs:
            raise Exception(f"IV already connected to {params.location}")
        self.connected_ivs[params.location] = params
        return f"IV access established in {params.location.value}"

    @staticmethod
    def connection_params_markdown() -> List[str]:
        return IVAccessManager._params_to_md(IVAccessParams)
    
    def get_state(self) -> str:
        if len(self.connected_ivs) == 0:
            return "No IV access"
        else:
            output = "IV access established in " + ", ".join([f"{loc.value}" for loc in self.connected_ivs.keys()])
            return output
    
class IOAccessLocation(Enum):
    PROXIMAL_TIBIA = "proximal tibia"
    DISTAL_FEMUR = "distal femur"
    DISTAL_TIBIA = "distal tibia"
    PROXIMAL_HUMERUS = "proximal humerus"
    STERNUM = "sternum"
    RADIUS_AND_ULNA = "radius and ulna"
    CALCANEUS = "calcaneus"


class IOAccessParams(BaseModel):
    location: IOAccessLocation
    needle_size: str = Field(..., pattern=r'\d+G', description='Gauge of needle, eg "18G", "20G", "22G"')


class IOAccessManager(DeviceConnectionManager_Base):
    def __init__(self) -> None:
        self.connected_ios: Dict[IOAccessLocation, IOAccessParams] = {}

        self.action_name = "Obtain IO access ($location, $size)"

    def connect(self, params: IOAccessParams):
        if params.location in self.connected_ios:
            raise Exception(f"IO already connected to {params.location}")
        
        self.connected_ios[params.location] = params

    @staticmethod
    def connection_params_markdown() -> List[str]:
        return IOAccessManager._params_to_md(IOAccessParams)
    
    def get_state(self) -> str:
        if len(self.connected_ios) == 0:
            return "No IO access"
        else:
            output = "IO access established in " + ", ".join([f"{loc.value}" for loc in self.connected_ios.keys()])
            return output


class EKGConnectionParams(BaseModel):
    pass

class EKGConnectionManager(DeviceConnectionManager_Base):
    def __init__(self) -> None:
        self.ekg_connected: bool = False
        self.action_name = "Connect EKG/ECG"

    def connect(self, params: EKGConnectionParams):
        if self.ekg_connected:
            raise Exception(f"EKG already connected")
        
        self.ekg_connected = True

    @staticmethod
    def connection_params_markdown() -> List[str]:
        return EKGConnectionManager._params_to_md(EKGConnectionParams)
    
    def get_state(self) -> str:
        if not self.ekg_connected:
            return "EKG not connected"
        else:
            return "EKG connected"
        
    def exposed_vitals(self) -> List[Vitals]:
        if not self.ekg_connected:
            return []
        return [Vitals.HEART_RATE, Vitals.RESPIRATORY_RATE]
    

class NIBPMonitorParams(BaseModel):
    pass

class NIBPMonitorManager(DeviceConnectionManager_Base):
    def __init__(self) -> None:
        self.nibp_connected: bool = False
        self.nibp_params: Optional[NIBPMonitorParams] = None
        self.action_name = "Connect BP monitor"

    def connect(self, params: NIBPMonitorParams):
        if self.nibp_connected:
            raise Exception("NIBP already connected")
        
        self.nibp_connected = True
        self.nibp_params = params

    @staticmethod
    def connection_params_markdown() -> List[str]:
        return NIBPMonitorManager._params_to_md(NIBPMonitorParams)

    def get_state(self) -> str:
        if not self.nibp_connected:
            return "NIBP monitor not connected"
        else:
            return f"NIBP monitor connected"

    def exposed_vitals(self) -> List[Vitals]:
        if not self.nibp_connected:
            return []
        return [Vitals.BLOOD_PRESSURE]


class PulseOximeterParams(BaseModel):
    probe_position: str = Field(..., description='Type of probe used, e.g., "Finger", "Earlobe", "Foot"')

class PulseOximeterManager(DeviceConnectionManager_Base):
    def __init__(self) -> None:
        self.connection_params: Optional[PulseOximeterParams] = None
        self.action_name = "Connect pulse oximeter"

    def connect(self, params: PulseOximeterParams):
        if self.connection_params is not None:
            raise Exception("Pulse Oximeter already connected")
        
        self.connection_params = params

    @staticmethod
    def connection_params_markdown() -> List[str]:
        return PulseOximeterManager._params_to_md(PulseOximeterParams)

    def get_state(self) -> str:
        if self.connection_params is None:
            return "Pulse Oximeter not connected"
        else:
            return f"Pulse Oximeter connected on {self.connection_params.probe_position}"

    def exposed_vitals(self) -> List[Vitals]:
        if self.connection_params is None:
            return []
        return [Vitals.HEART_RATE, Vitals.RESPIRATORY_RATE]


class VentilatorParams(BaseModel):
    mode: str = Field(..., description='Ventilation mode, e.g., "AC", "PC", "PSV"')
    fio2: float = Field(..., description='Fraction of Inspired Oxygen, a value between 0.21 and 1.0')

class VentilatorManager(DeviceConnectionManager_Base):
    def __init__(self) -> None:
        self.connection_params: Optional[VentilatorParams] = None

    def connect(self, params: VentilatorParams):
        if self.connection_params is not None:
            raise Exception("Ventilator already connected")
        
        self.connection_params = params

    @staticmethod
    def connection_params_markdown() -> List[str]:
        return VentilatorManager._params_to_md(VentilatorParams)

    def get_state(self) -> str:
        if self.connection_params is None:
            return "Ventilator not connected"
        else:
            return f"Ventilator connected in {self.connection_params.mode} mode, FiO2: {self.connection_params.fio2}"

    def exposed_vitals(self) -> List[Vitals]:
        if self.connection_params is None:
            return []
        return [Vitals.RESPIRATORY_RATE] # [Vitals.CO2_LEVEL]
    

class ContinuousGlucometerParams(BaseModel):
    pass

class ContinuousGlucometerManager(DeviceConnectionManager_Base):
    def __init__(self) -> None:
        self.connection_params: Optional[ContinuousGlucometerParams] = None

    def connect(self, params: ContinuousGlucometerParams):
        if self.connection_params is not None:
            raise Exception("Continuous Glucometer already connected")
        
        self.connection_params = params

    @staticmethod
    def connection_params_markdown() -> List[str]:
        return ContinuousGlucometerManager._params_to_md(ContinuousGlucometerParams)
    
    def get_state(self) -> str:
        if self.connection_params is None:
            return "Continuous Glucometer not connected"
        else:
            return f"Continuous Glucometer connected"
        
    def exposes_vitals(self) -> List[Vitals]:
        return [Vitals.BLOOD_GLUCOSE]



class DeviceManager:
    def __init__(self) -> None:
        self.iv_manager = IVAccessManager()
        self.io_manager = IOAccessManager()
        self.ekg_manager = EKGConnectionManager()
        self.nibp_manager = NIBPMonitorManager()
        self.pulse_ox_manager = PulseOximeterManager()
        self.ventilator_manager = VentilatorManager()
        self.continuous_glucometer_manager = ContinuousGlucometerManager()

        self.all_managers: List[DeviceConnectionManager_Base] = [
            self.iv_manager,
            self.io_manager,
            self.ekg_manager,
            self.nibp_manager,
            self.pulse_ox_manager,
            self.ventilator_manager,
            self.continuous_glucometer_manager,
        ]

    def full_state_markdown(self) -> List[str]:
        states: List[str] = []
        for manager in self.all_managers:
            states.append(manager.get_state())
        
        return states
    
    def get_manager_from_call_data(self, call_data: ActionDatabase.CallData) -> DeviceConnectionManager_Base | None:
        for manager in self.all_managers:
            if call_data.name.lower() in manager.action_name.lower():
                return manager
        return None


if __name__ == "__main__":
    async def main():
        device_manager = DeviceManager()

        action_db = ActionDatabase()
        action = action_db.get_relevant_actions("Get IV access")[0]
        task_call = action_db.get_action_from_call(action.examples[0].action, action.examples[0].input)

        print(task_call.full_input)

        connection_manager = device_manager.get_manager_from_call_data(task_call.call_data)
        result = connection_manager.handle_call(task_call.call_data)
        print(result)

        print(device_manager.full_state_markdown())

    asyncio.run(main())