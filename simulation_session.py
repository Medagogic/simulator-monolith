import enum
from fastapi import APIRouter
from pydantic import BaseModel
import asyncio

import socketio
from webhandler_chat import ChatWebHandler


class SimulationSessionState(enum.Enum):
    NOT_STARTED = 0
    RUNNING = 1
    PAUSED = 2
    FINISHED = 3


class SimulationSessionData(BaseModel):
    state: SimulationSessionState = SimulationSessionState.NOT_STARTED
    exercise_name: str


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