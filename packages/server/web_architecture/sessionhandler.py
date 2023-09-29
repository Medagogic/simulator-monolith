from fastapi import APIRouter
import socketio


class SessionHandler_Base:
    def __init__(self, session_id: str, sio: socketio.AsyncServer):
        self.session_id = session_id
        self.sio = sio

        self.router = APIRouter(prefix=f"/sessions/{session_id}")



