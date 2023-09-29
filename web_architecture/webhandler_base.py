from __future__ import annotations
from typing import Any, Type, TYPE_CHECKING
from fastapi import APIRouter

import socketio

if TYPE_CHECKING:
    from web_architecture.sessionhandler_base import SessionHandler_Base


class WebHandler_Base(socketio.AsyncNamespace):
    def __init__(self, namespace: str, sesh_handler: SessionHandler_Base):
        self.api_namespace = namespace
        self.sesh_handler = sesh_handler

        super().__init__(f"/{self.sesh_handler.session_id}/{self.api_namespace}")
        sesh_handler.sio.register_namespace(self)

        self.router = APIRouter()

    @property
    def session_id(self) -> str:
        return self.sesh_handler.session_id

    async def emit(self, event: str, data: Any, room: Any = None, skip_sid: Any = None, namespace: Any = None, callback: Any = None) -> None:
        print(f"emit {event} in {namespace}")
        await socketio.AsyncNamespace.emit(self, event, data, room=room, skip_sid=skip_sid, namespace=namespace, callback=callback)

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

    
    async def on_connect(self, sid, environ):
        print(f"Client connected to WebHandler_Base with ID {sid}")
