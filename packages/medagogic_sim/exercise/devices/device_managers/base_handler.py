from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, List, Dict, Optional, Type

from packages.medagogic_sim.action_db.actions_for_brains import ActionModel

if TYPE_CHECKING:
    from packages.medagogic_sim.action_db.actions_for_brains import ActionDatabase

from enum import Enum
from pydantic import BaseModel, Field
from packages.medagogic_sim.exercise.devices.device_utils import FuzzyEnumMatcher
import re
import jsonschema2md

from packages.medagogic_sim.logger.logger import get_logger, logging
from packages.medagogic_sim.exercise.simulation_types import Vitals


class DeviceHandler_Base(ABC):
    action_name: str = "NOT SET"

    @staticmethod
    @abstractmethod
    def connection_params_markdown() -> List[str]:
        pass
    
    @abstractmethod
    def get_state(self) -> str:
        pass
    
    def exposed_vitals(self) -> List[Vitals]:
        return []
    
    @abstractmethod
    def handle_call(self, call_data: ActionDatabase.CallData) -> str:
        pass

    @property
    @abstractmethod
    def is_connected(self) -> bool:
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
        schema = DeviceHandler_Base.__inline_schema_refs(schema)
        parser = jsonschema2md.Parser()
        md_lines = parser.parse_schema({"properties": schema})
        md_lines = [l.strip() for l in md_lines if l.strip() != ""]
        params = md_lines[2:]
        
        return params
    
    @staticmethod
    @abstractmethod
    def get_action_model() -> ActionModel:
        pass