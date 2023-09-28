

import enum
from typing import Any, Type
from fastapi import APIRouter, FastAPI
from pydantic import BaseModel
import asyncio

import socketio
from web_handler_module import WebHandlerModuleBase


class SimulationSessionState(enum.Enum):
    NOT_STARTED = 0
    RUNNING = 1
    PAUSED = 2
    FINISHED = 3


class SimulationSessionData(BaseModel):
    state: SimulationSessionState = SimulationSessionState.NOT_STARTED
    exercise_name: str


class WebHandler_Base(socketio.AsyncNamespace):
    def __init__(self, namespace: str, sesh_handler: "SimulationSessionHandler"):
        self.api_namespace = namespace
        self.sesh_handler = sesh_handler

        super().__init__(f"/{self.sesh_handler.session_id}/{self.api_namespace}")
        sesh_handler.sio.register_namespace(self)

        self.router = APIRouter()

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


class ChatWebHandler(WebHandler_Base):
    def __init__(self, sesh_handler: "SimulationSessionHandler"):
        WebHandler_Base.__init__(self, namespace="chat", sesh_handler=sesh_handler)

        self.router.get("/self-router-get")(self.handle_test)


    async def handle_test(self):
        return {"content": f"Hello world in session"}


    async def on_message(self, sid, msg):
        print(f"on_message {msg} in {self.namespace}")
        await self.emit("response", {"content": f"{msg} @ {self.namespace}"})  # or send to everyone


class SimulationSessionHandler:
    def __init__(self, session_id: str, sio: socketio.AsyncServer):
        self.data = SimulationSessionData(exercise_name="Exercise 1")
        self.session_id = session_id
        self.sio = sio

        self.router = APIRouter(prefix="")
        self.chat_handler = ChatWebHandler(self)


    def start(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.main_loop())

    async def main_loop(self):
        while self.data.state == SimulationSessionState.RUNNING:
            await asyncio.sleep(1)
            print("Running")