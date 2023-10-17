from __future__ import annotations
from functools import wraps
import json
from typing import Any, Callable, Dict, List, Type
from packages.server.web_architecture.sio_api_handlers import get_field_info
from pydantic import BaseModel


def process_event_type(event_type):
    if isinstance(event_type, type) and issubclass(event_type, BaseModel):
        return event_type.model_json_schema()
    else:
        return get_field_info(event_type)


def emits(event_name: str, event_type: Type) -> Callable:
    def decorator_emit(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            return func(*args, **kwargs)

        wrapper.__setattr__("_emit_info", (event_name, event_type))
        return wrapper
    return decorator_emit


class SIOEmitSchema(BaseModel):
    event_name: str
    data_schema: Dict
    real_type: Any = None


class SIOEmitter(type):
    def __new__(cls, name, bases, dct):
        # Create the new class.
        new_class = super().__new__(cls, name, bases, dct)

        # Initialize EVENT_DATA if it doesn't exist in the current class.
        if 'EVENT_DATA' not in dct:
            new_class.EVENT_DATA: List[SIOEmitSchema] = []   # type: ignore

        cls.process_emits(new_class)

        return new_class

    @staticmethod
    def process_emits(new_class):
        for attr_name in dir(new_class):
            attr = getattr(new_class, attr_name)
            if callable(attr) and hasattr(attr, '_emit_info'):
                event_name, event_type = attr._emit_info

                openapi_schema = process_event_type(event_type)
                emit_info = SIOEmitSchema(event_name=event_name, data_schema=openapi_schema, real_type=event_type)

                if emit_info not in new_class.EVENT_DATA:
                    new_class.EVENT_DATA.append(emit_info)

    @staticmethod
    def _generate_schema(emit_data: List[SIOEmitSchema]):
        schema: Dict = {}

        for emit_info in emit_data:
            event_name = emit_info.event_name
            type_schema = emit_info.data_schema
            schema[event_name] = type_schema

        return schema

    @staticmethod
    def _get_emit_event_schema(new_class):
        return SIOEmitter._generate_schema(new_class.EVENT_DATA)


if __name__ == "__main__":
    class TestDataType(BaseModel):
        name: str
        age: int


    class Session(metaclass=SIOEmitter):
        @emits("test_event", Dict[str, str])
        def test_func(self):
            self.emit("test_event", {"test_param": "test_value"})

        @emits("add_person", TestDataType)
        def age_func(self):
            self.emit("add_person", TestDataType(name="John", age=20))

        def emit(self, event: str, params: Any) -> None:
            pass

        @classmethod
        def list_emit_calls(cls):
            schema = SIOEmitter._get_emit_event_schema(cls)
            print(json.dumps(schema, indent=4))

    Session.list_emit_calls()
