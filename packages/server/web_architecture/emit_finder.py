from __future__ import annotations
import ast
from functools import wraps
import inspect
import json
from typing import Any, Callable, Dict, List, Type
from socketio_api import get_field_info

# Assuming Pydantic is available
from pydantic import BaseModel


def is_pydantic_model(annotation) -> bool:
    """
    Check if the annotation is a Pydantic model. This is a simplistic check.
    """
    return inspect.isclass(annotation) and issubclass(annotation, BaseModel)


def emits(event_name: str, event_type: Type) -> Callable:
    def decorator_emit(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            return func(*args, **kwargs)

        wrapper.__setattr__("_emit_info", (event_name, event_type))
        return wrapper
    return decorator_emit


def process_event_type(event_type):
    if isinstance(event_type, type) and issubclass(event_type, BaseModel):
        return event_type.model_json_schema()
    else:
        return get_field_info(event_type)


class EmitInfo(BaseModel):
    event_name: str
    openapi_schema: Dict

def generate_schema(cls: type[Session]):
    schema: Dict = {}

    for emit_info in cls.EVENT_DATA:
        event_name = emit_info.event_name
        type_schema = emit_info.openapi_schema
        schema[event_name] = type_schema

    return schema


def process_emits(cls: type[Session]):
    # Inspect the attributes of the class to find methods that have been decorated with `emits`
    for attr_name in dir(cls):
        attr = getattr(cls, attr_name)
        if callable(attr) and hasattr(attr, '_emit_info'):
            event_name, event_type = attr._emit_info

            openapi_schema = process_event_type(event_type)
            emit_info = EmitInfo(event_name=event_name, openapi_schema=openapi_schema)

            if emit_info not in cls.EVENT_DATA:
                cls.EVENT_DATA.append(emit_info)
            
    return cls



class TestDataType(BaseModel):
    name: str
    age: int

@process_emits
class Session:
    EVENT_DATA: List[EmitInfo] = []

    @emits("test_event", Dict[str, str])
    def test_func(self):
        self.emit("test_event", {"test_param": "test_value"})

    @emits("add_person", TestDataType)
    def age_func(self):
        self.emit("add_person", TestDataType(name="John", age=20))

    def emit(self, event: str, params: Any) -> None:
        pass  # The emit method implementation

    @classmethod
    def list_emit_calls(cls):
        # for emit_info in cls.EVENT_DATA:
        #     print(emit_info)
        schema = generate_schema(cls)
        print(json.dumps(schema, indent=4))


# Test the class method
Session.list_emit_calls()
