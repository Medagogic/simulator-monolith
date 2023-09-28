from datetime import datetime
from typing import Dict, Optional
from fastapi import APIRouter, FastAPI
from pydantic import BaseModel, Field
import socketio
import human_id
from simulation_session import SimulationSessionHandler


class SessionData(BaseModel):
    session_id: str
    sids_in_session: list[str]
    creation_datetime: datetime = Field(default_factory=datetime.utcnow)


class SessionManager():
    def __init__(self, sio: socketio.AsyncServer, app: FastAPI):
        self.sio = sio
        self.app = app
        self.sessionIdByUser: Dict[str, str] = {}
        self.sessionDataBySessionId: Dict[str, SessionData] = {}
        self.sessionsBySessionId: Dict[str, SimulationSessionHandler] = {}

        self.router = APIRouter(prefix="/session")
        self.router.add_api_route("/new", self.handle_create_session, methods=["POST"])
        self.router.add_api_route("/list", self.handle_list_sessions, methods=["GET"])

        self.app.include_router(self.router)


    async def handle_create_session(self):
        session_id = self.create_session()
        return session_id


    async def handle_list_sessions(self):
        return [d for d in self.sessionDataBySessionId.values()]
    

    def create_session(self, sid: Optional[str]=None) -> str:
        session_id = human_id.generate_id()
        session_data = SessionData(session_id=session_id, sids_in_session=[])
        session = SimulationSessionHandler(session_id, self.sio)

        if sid:
            self.sessionIdByUser[sid] = session_id
            session_data.sids_in_session.append(sid)

        self.sessionDataBySessionId[session_id] = session_data
        self.sessionsBySessionId[session_id] = session

        # self.app.add_api_route(f"/session/{session_id}/chat", self.handle_test, methods=["GET"])
        self.app.include_router(session.router, prefix=f"/session/{session_id}")
        self.app.openapi_schema = None
        self.app.setup()

        for k, v in self.sio.namespace_handlers.items():
            print(k)
            print(v)

        return session_id
    

    async def handle_test(self):
        return {"content": "Hello world"}
    

    def remove_user_from_session(self, sid: str, delete_session_if_empty=True) -> None:
        if sid not in self.sessionIdByUser:
            return
        
        session_id = self.sessionIdByUser[sid]
        del self.sessionIdByUser[sid]

        self.sessionDataBySessionId[session_id].sids_in_session.remove(sid)

        if delete_session_if_empty:
            if len(self.sessionDataBySessionId[session_id].sids_in_session) == 0:
                del self.sessionDataBySessionId[session_id]

