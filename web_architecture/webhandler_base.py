from __future__ import annotations
import inspect
from typing import Any, Callable, Dict, Type, TYPE_CHECKING
from fastapi import APIRouter
from pydantic import BaseModel, create_model

import socketio

if TYPE_CHECKING:
    from web_architecture.sessionhandler_base import SessionHandler_Base


class MyDataType(BaseModel):
    something: str
    some_number: int


def get_json_type(py_type: Type[Any]) -> str:
    # Create a temporary Pydantic model with a single field of the specified type
    TempModel = create_model("TempModel", field=(py_type, ...))
    
    # Generate the schema for the temporary model
    schema = TempModel.model_json_schema()
    
    # Extract and return the JSON type of the field from the schema
    json_type = schema['properties']['field']['type']
    return json_type


class SocketEventMeta(type):
    def __init__(cls: Type[WebHandler_Base], name, bases, dct: Dict[str, Any]):
        super().__init__(name, bases, dct)

        # Look for socket event handlers in the class dictionary
        for attr_name, attr_value in dct.items():
            if callable(attr_value) and attr_name.startswith("on_"):
                # Assume the event name is the method name minus the "on_" prefix
                event_name = attr_name[3:]
                # Assume the event data type is the type of the second argument (after 'self')
                params = getattr(attr_value, "__annotations__", {})
                data_type_name = params.get('data', None)  # Assumes the parameter name is 'data'

                schema = None

                if data_type_name:
                    schema_type: Type[BaseModel] = globals().get(data_type_name, None)
                    if schema_type:
                        schema = schema_type.model_json_schema()
                    else:
                        param_type = get_json_type(eval(data_type_name))
                        schema = {"type": param_type}
                else:
                    if event_name not in ["connect", "disconnect"]:
                        raise Exception(f"Could not find parameter 'data' for socketio event '{attr_name}'")

                cls._socketio_event_registry[event_name] = schema


class WebHandler_Base(socketio.AsyncNamespace, metaclass=SocketEventMeta):
    _socketio_event_registry = {}

    def __init__(self, namespace: str, sesh_handler: SessionHandler_Base):
        self.api_namespace = namespace
        self.sesh_handler = sesh_handler

        super().__init__(f"/{self.sesh_handler.session_id}/{self.api_namespace}")
        sesh_handler.sio.register_namespace(self)

        self.router = APIRouter()


    # To make sure that the router is added to the session handler after the subclass is initialized and has added routes
    def __init_subclass__(cls: Type["WebHandler_Base"], **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        original_init = cls.__init__

        def new_init(self: "WebHandler_Base", *args: Any, **kwargs: Any) -> None:
            original_init(self, *args, **kwargs)
            self.__post_init()

        cls.__init__ = new_init


    # Add the router to the session handler
    def __post_init(self) -> None:
        self.sesh_handler.router.include_router(self.router, prefix=f"/{self.api_namespace}")


    @property
    def session_id(self) -> str:
        return self.sesh_handler.session_id

    
    async def on_connect(self, sid, environ):
        print(f"Client connected to WebHandler_Base with ID {sid}")


    async def on_some_message(self, sid, data: MyDataType):
        pass


    @classmethod
    def generate_doc(cls):
        doc = {"input_events": cls._socketio_event_registry}
        return doc
    

if __name__ == "__main__":
    def main():
        doc = WebHandler_Base.generate_doc()
        print(doc)

    main()