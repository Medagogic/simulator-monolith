from fastapi import FastAPI, Depends, Query
from typing import Dict

existing_sessions: Dict[str, "Session"] = {}


class Session:
    def __init__(self, session_id: str):
        self.session_id = session_id

    async def get_data(self):
        # Logic for retrieving session data. Here's a placeholder implementation.
        return {"session_id": self.session_id, "data": "Some data related to this session"}

class NewSessionRouter:
    def __init__(self, app: FastAPI) -> None:
        self.app = app
        self.existing_sessions: Dict[str, Session] = {}

    def create_session(self, session_id: str) -> Session:
        if session_id not in self.existing_sessions:
            session = Session(session_id)
            self.existing_sessions[session_id] = session
            return session
        else:
            raise ValueError("Session already exists")

    def get_session(self, session_id: str) -> Session:
        session = self.existing_sessions.get(session_id)
        if session is None:
            # raise HTTPException(status_code=404, detail="Session not found")
            session = self.create_session(session_id)   
        return session


def init_new_session_router_routes(session_manager: NewSessionRouter):
    @session_manager.app.get("/new-session-router/sessions/{session_id}/data")
    async def read_session_data(session: Session = Depends(session_manager.get_session), poop: str = Query(...)):
        return {"poop": poop, "session": await session.get_data()}