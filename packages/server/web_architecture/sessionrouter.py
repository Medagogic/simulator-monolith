from __future__ import annotations
from functools import wraps
from fastapi import APIRouter, FastAPI, Depends, HTTPException, Query
from typing import Any, Callable, Dict, Generic, Type, TypeVar

import human_id
import socketio

class Session():
    def __init__(self, session_id: str, sio: socketio.AsyncServer):
        self.session_id = session_id
        self.sio = sio

    async def on_test_event(self, sid, data):
        print(f"Yooooo, test event received from {sid}: {data} in session {self.session_id}")

    async def on_test_event_2(self, sid, data):
        print(f"Oi, test event 2 received from {sid}: {data} in session {self.session_id}")

    async def handle_magic_event(self, sid, data):
        return f"Magic event finished from {sid}: {data} in session {self.session_id}"


T = TypeVar('T', bound=Session)

class SessionRouter(socketio.AsyncNamespace, Generic[T]):
    def __init__(self, app: FastAPI, sio: socketio.AsyncServer, session_cls: Type[T]) -> None:
        super().__init__(namespace="/session")
        self.sio = sio

        self.app = app
        self.session_cls = session_cls
        self.existing_sessions: Dict[str, T] = {}
        self.router = APIRouter(prefix="/new-session-router")
        self.session_router = APIRouter(prefix="/session/{session_id}")
        self.init_routes()

        self.router.include_router(self.session_router)
        self.app.include_router(self.router)

        self.sio.register_namespace(self)


    def create_session(self, session_id: str) -> T:
        if session_id not in self.existing_sessions:
            session = self.session_cls(session_id, self.sio)
            self.existing_sessions[session_id] = session
            return session
        else:
            raise ValueError("Session already exists")
        
    async def trigger_event(self, event, sid, *args):
        if not hasattr(self, f"on_{event}"):
            try:
                session = self.get_session_for_sid(sid)
                func = getattr(session, f"on_{event}", None)
                if func is not None:
                    return await func(sid, *args)
            except:
                pass
            print(f"SIO ERROR: {event} not found")
            return False

        return await super().trigger_event(event, sid, *args)

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

    async def on_connect(self, sid, environ):
        print(f"Client {sid} connected.")

    async def on_disconnect(self, sid):
        print(f"Client {sid} disconnected.")

    async def on_join_session(self, sid, session_id: str):
        current_rooms = self.sio.rooms(sid, namespace=self.namespace)
        for room in current_rooms[1:]:
            print(f"Client {sid} left session {room}")
            self.sio.leave_room(sid, room, namespace=self.namespace)

        print(f"Client {sid} joined session {session_id}.")
        self.sio.enter_room(sid, session_id, namespace=self.namespace)

    async def on_leave_session(self, sid, data):
        current_rooms = self.sio.rooms(sid, namespace=self.namespace)
        for room in current_rooms[1:]:
            print(f"Client {sid} left session {room}")
            self.sio.leave_room(sid, room, namespace=self.namespace)

    def get_session_for_sid(self, sid) -> T:
        rooms = self.sio.rooms(sid, namespace=self.namespace)
        if len(rooms) <= 1:
            raise Exception(f"{sid} is not in a session")
        room_id = rooms[1]
        
        if room_id not in self.existing_sessions:
            raise Exception(f"Session {room_id} not found")

        return self.existing_sessions[room_id]

    async def on_magic_event(self, sid, data):
        session = self.get_session_for_sid(sid)
        return await session.handle_magic_event(sid, data)


if __name__ == "__main__":
    import uvicorn
    from fastapi import FastAPI
    import asyncio
    import socketio

    sio = socketio.AsyncServer(async_mode="asgi", namespaces=["/session"])
    app = FastAPI()
    app_asgi = socketio.ASGIApp(sio, app)

    session_router = SessionRouter(app, sio, Session)

    session_name = "test-session"

    async def start_test_client(session_id: str):
        test_client = socketio.AsyncClient()
        test_client.on('connect', lambda: print("Connected to server"))

        def callback(data=None):
            print(f"Callback received: {data}")

        await test_client.connect('http://localhost:8000', namespaces=["/session"])
        await asyncio.sleep(1)
        await test_client.emit('join_session', session_id, namespace="/session")
        await test_client.emit('test_event', {'example': 'data'}, namespace="/session")
        await test_client.emit("magic_event", {"example": "data"}, namespace="/session", callback=callback)

        await asyncio.sleep(1)

        print("Joining unused session and sending test_event_2")
        await test_client.emit('join_session', "unused-sesh", namespace="/session")
        await test_client.emit('test_event_2', {'example': 'data'}, namespace="/session", callback=callback)

        await asyncio.sleep(1)
        print("Sending unknown event")
        await test_client.emit('unknown_event', {'example': 'data'}, namespace="/session")

        await asyncio.sleep(1)
        print("Sending event when not in session")
        await test_client.emit('leave_session', "unused-sesh", namespace="/session")

        await test_client.emit('test_event', {'example': 'data'}, namespace="/session")

        await asyncio.sleep(1)
        await test_client.disconnect()

    async def main():
        config = uvicorn.Config(app_asgi, host="0.0.0.0", port=8000, log_level="info")
        server = uvicorn.Server(config)

        server_task = asyncio.create_task(server.serve())

        session_router.create_session(session_id=session_name)
        session_router.create_session(session_id="unused-sesh")
        client_task = asyncio.create_task(start_test_client(session_id=session_name))

        await client_task

        await asyncio.sleep(1)

        server.should_exit = True
        await server_task


    asyncio.run(main())