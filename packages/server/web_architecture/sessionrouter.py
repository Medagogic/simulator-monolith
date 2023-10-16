from __future__ import annotations
from fastapi import APIRouter, FastAPI, Depends, HTTPException, Query
from typing import Dict, Generic, Type, TypeVar

import human_id
import socketio


class Session:
    def __init__(self, session_id: str, sio: socketio.AsyncServer):
        self.session_id = session_id
        self.sio = sio

T = TypeVar('T', bound=Session)

class NewSessionRouter(Generic[T]):
    def __init__(self, app: FastAPI, sio: socketio.AsyncServer, session_cls: Type[T]) -> None:
        self.app = app
        self.sio = sio
        self.session_cls = session_cls
        self.existing_sessions: Dict[str, T] = {}
        self.router = APIRouter(prefix="/new-session-router")
        self.session_router = APIRouter(prefix="/session/{session_id}")
        self.init_routes()

        self.router.include_router(self.session_router)
        self.app.include_router(self.router)

    def create_session(self, session_id: str) -> T:
        if session_id not in self.existing_sessions:
            session = self.session_cls(session_id, self.sio)
            self.existing_sessions[session_id] = session
            return session
        else:
            raise ValueError("Session already exists")

    def get_session(self, session_id: str) -> T:
        session = self.existing_sessions.get(session_id)
        if session is None:
            raise HTTPException(status_code=404, detail="Session not found")
        return session
    
    def destroy_session(self, session_id: str):
        if session_id in self.existing_sessions:
            del self.existing_sessions[session_id]
        else:
            raise HTTPException(status_code=404, detail="Session not found")
    
    def init_routes(self):
        @self.session_router.get("/test-session")
        async def test_endpoint(session: T = Depends(self.get_session)):
            return {"session_id": session.session_id, "session_type": type(session).__name__}
        
        @self.router.get("/list-sessions")
        async def list_sessions():
            return list(self.existing_sessions.keys())
        
        @self.router.get("/create-session")
        async def create_session():
            id = human_id.generate_id()
            session = self.create_session(id)
            return {"session_id": session.session_id}

