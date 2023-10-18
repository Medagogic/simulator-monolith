from __future__ import annotations
from functools import wraps
import inspect
from typing import Any, Awaitable, Callable, Coroutine, Dict, List, Optional, Type, TypeVar, cast
from packages.tools.scribe.src.scribe_helpers import get_field_info, get_sio_data_type
from pydantic import BaseModel


def type_to_schema_dict(event_type: Any):
    if isinstance(event_type, type) and issubclass(event_type, BaseModel):
        return event_type.model_json_schema()
    else:
        return get_field_info(event_type)


class ScribeEmitSchema(BaseModel):
    emits_event: str
    data_schema: Dict
    data_type: Any

class ScribeHandlerSchema(BaseModel):
    handler_name: str
    data_schema: Dict
    data_type: Any


def check_params(func: Callable) -> None:
    if func.__name__ in ["on_connect", "on_disconnect"]:
        return

    sig = inspect.signature(func)
    params = list(sig.parameters.values())

    # Define a helper function to check 'sid' and 'data' parameters.
    def check_sid_and_data(params_list, sid_index, data_index):
        if len(params_list) <= max(sid_index, data_index):
            return False
        correct_sid = params_list[sid_index].name == 'sid' and (params_list[sid_index].annotation is str or params_list[sid_index].annotation == inspect.Parameter.empty)    
        if not correct_sid:
            raise TypeError(f"sid is not of type 'str' - '{func.__name__}' must take (sid: str, data)")
        
        # # Ensure data variable is named 'data'
        # actual_data_param_name = params_list[data_index].name
        # correct_data = actual_data_param_name == 'data' 
        # if not correct_data:
        #     raise TypeError(f"'{actual_data_param_name}' must be named 'data' - '{func.__name__}' must take (sid: str, data)")

    # Check for methods (self, sid, data) or functions (sid, data)
    if len(params) == 3:
        check_sid_and_data(params, 1, 2)
    elif len(params) == 2:
        check_sid_and_data(params, 0, 1)
    else:
        raise TypeError(f"Function '{func.__name__}' must take (sid: str, data)")


# Decorator for Socket.IO event emitters
def scribe_emits(event_name: str, data_type: Type) -> Callable:
    def decorator_emit(func: Callable) -> Callable:
        if inspect.iscoroutinefunction(func):
            @wraps(func)
            async def wrapper(*args, **kwargs) -> Any:
                return await func(*args, **kwargs)
        else:
            @wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                return func(*args, **kwargs)
        
        data_schema = type_to_schema_dict(data_type)
        schema = ScribeEmitSchema(emits_event=event_name, data_schema=data_schema, data_type=data_type)

        wrapper.__setattr__("_emit_info", schema)
        return wrapper
    return decorator_emit

# Decorator for Socket.IO event handlers
SIO_HANDLER_SID_DATA = TypeVar('SIO_HANDLER_SID_DATA', bound=Callable[[Any, str, Any], Awaitable[Any]])
def scribe_handler(func: SIO_HANDLER_SID_DATA) -> SIO_HANDLER_SID_DATA:
    check_params(func)

    if not inspect.iscoroutinefunction(func):
        raise TypeError(f"Function '{func.__name__}' is not async, 'scribe_handler' only supports async functions.")

    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        return await func(*args, **kwargs)

    event_name = func.__name__
    data_type = get_sio_data_type(func)
    data_schema = type_to_schema_dict(data_type)
    handler_schema = ScribeHandlerSchema(handler_name=event_name, data_schema=data_schema, data_type=data_type)

    wrapper.__setattr__("_handler_info", handler_schema)
    return cast(SIO_HANDLER_SID_DATA, wrapper)


class ScribeMixin_Emit:
    __SIO_EMIT_DATA: List[ScribeEmitSchema] = []

    @classmethod
    def __find_tagged_emit_methods(cls) -> None:
        cls.__SIO_EMIT_DATA = []
        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if callable(attr) and hasattr(attr, '_emit_info'):
                emit_schema = attr._emit_info
                if emit_schema not in cls.__SIO_EMIT_DATA:
                    cls.__SIO_EMIT_DATA.append(emit_schema)

    @classmethod
    def scribe_get_emit_schema(cls) -> List[ScribeEmitSchema]:
        cls.__find_tagged_emit_methods()
        return cls.__SIO_EMIT_DATA
    
    

class ScribeMixin_Handler:
    __SIO_HANDLER_DATA: List[ScribeHandlerSchema] = []
    __SCRIBE_HANDLERS_BY_EVENT: Dict[str, Callable] = {}

    @classmethod
    def __find_tagged_handler_methods(cls) -> None:
        cls.__SIO_HANDLER_DATA = []
        cls.__SCRIBE_HANDLERS_BY_EVENT = {}
        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if callable(attr) and hasattr(attr, '_handler_info'):
                handler_schema: ScribeHandlerSchema = attr._handler_info
                cls.__SIO_HANDLER_DATA.append(attr._handler_info)
                cls.__SCRIBE_HANDLERS_BY_EVENT[handler_schema.handler_name] = attr

    @classmethod
    def scribe_get_handler_schema(cls) -> List[ScribeHandlerSchema]:
        cls.__find_tagged_handler_methods()
        return cls.__SIO_HANDLER_DATA
    
    @classmethod
    def scribe_get_handler(cls, event_name: str) -> Optional[Callable]:
        return cls.__SCRIBE_HANDLERS_BY_EVENT.get(event_name, None)
    
    def init_sio_handlers(self):
        self.__find_tagged_handler_methods()


if __name__ == "__main__":
    class TestDataType(BaseModel):
        name: str
        age: int

    class TestEmitterHandler(ScribeMixin_Emit, ScribeMixin_Handler):
        @scribe_emits("test_event", Dict[str, str])
        def test_func(self):
            self.emit("test_event", {"test_param": "test_value"})

        @scribe_emits("add_person", TestDataType)
        def age_func(self):
            self.emit("add_person", TestDataType(name="John", age=20))

        @scribe_handler
        def on_test_event(self, sid, data: Dict[str, str]):
            print(f"Received {data} from {sid}")

        def emit(self, event: str, params: Any) -> None:
            pass

    for e in TestEmitterHandler.scribe_get_emit_schema():
        print(f"EMIT: {e.emits_event} - {e.data_type}")

    for h in TestEmitterHandler.scribe_get_handler_schema():
        print(f"HANDLER: {h.handler_name} - {h.data_type}")
