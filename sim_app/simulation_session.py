import enum
from fastapi import APIRouter
from pydantic import BaseModel
import asyncio

import socketio
from sim_app.webhandler_chat import ChatWebHandler
from web_architecture.sessionhandler import SessionHandler_Base

class SimulationSessionState(enum.Enum):
    NOT_STARTED = 0
    RUNNING = 1
    PAUSED = 2
    FINISHED = 3


class SimulationSessionData(BaseModel):
    state: SimulationSessionState = SimulationSessionState.NOT_STARTED
    exercise_name: str


class SimulationSessionHandler(SessionHandler_Base):
    def __init__(self, session_id: str, sio: socketio.AsyncServer):
        super().__init__(session_id, sio)
        self.data = SimulationSessionData(exercise_name="Exercise 1")
        self.chat_handler = ChatWebHandler(self)

        self.start()


    def start(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.main_loop())


    def stop(self):
        self.data.state = SimulationSessionState.FINISHED


    async def main_loop(self):
        while self.data.state != SimulationSessionState.FINISHED:
            await asyncio.sleep(1)
        print("Finished")