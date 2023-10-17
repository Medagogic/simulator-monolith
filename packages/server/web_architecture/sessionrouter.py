from __future__ import annotations
from functools import wraps
import inspect
import json
import sys
import traceback
from fastapi import APIRouter, FastAPI, Depends, HTTPException
from typing import Any, Callable, Dict, Generic, List, Protocol, Tuple, Type, TypeVar, get_args, get_type_hints
import human_id
from pydantic import BaseModel
import socketio
from packages.server.web_architecture.sio_api_handlers import _generate_socketio_openapi_schema
from packages.server.web_architecture.sio_api_emitters import SIOEmitSchema, SIOEmitter, emits

from colorama import Fore
import colorama

colorama.init(autoreset=True)


class Session(metaclass=SIOEmitter):
    SIO_EVENT_HANDLERS: Dict = {}

    def __init__(self, session_id: str, sio: socketio.AsyncServer):
        self.session_id = session_id
        self.sio = sio

    @classmethod
    def sio_handler(cls, func):
        @wraps(func)
        async def wrapper(self: Session, sid, *args, **kwargs):
            return await func(self, sid, *args, **kwargs)
        
        cls.SIO_EVENT_HANDLERS[func.__name__] = wrapper
        return wrapper
    
    def emit(self, event_name: str, data: Any) -> None:
        self.sio.emit(event_name, data, room=self.session_id, namespace="/session")


# Use this protocol to type hint an object (mixins for the SessionRouter) which can emit events
class SessionRouterProtocol(Protocol):
    def emit(self, event_name: str, data: Any) -> None:
        ...


T = TypeVar('T', bound=Session)
class SessionRouter(socketio.AsyncNamespace, Generic[T], metaclass=SIOEmitter):
    def __init__(self, app: FastAPI, sio: socketio.AsyncServer, session_cls: Type[T]=None) -> None:
        super().__init__(namespace="/session")
        self.sio = sio

        self.app = app
        self.session_cls = session_cls
        self.existing_sessions: Dict[str, T] = {}
        self.router = APIRouter(prefix="/new-session-router")
        self.session_router = APIRouter(prefix="/session/{session_id}")
        self.init_api_routes()

        self.router.include_router(self.session_router)
        self.app.include_router(self.router)

        self.sio.register_namespace(self)


    @classmethod
    def get_sio_handler_schema(cls, session_cls: Type[T]):
        members = inspect.getmembers(cls)
        cls_methods = [member for member in members if member[0].startswith('on_') and inspect.isfunction(member[1])]
        session_methods = [(k, v) for k, v in session_cls.SIO_EVENT_HANDLERS.items()]
        all_handlers: List[Tuple[str, Callable]] = cls_methods + session_methods

        schema = _generate_socketio_openapi_schema(all_handlers)
        return schema

    
    @classmethod
    def get_emitted_events(cls, session_cls: Type[T]) -> List[SIOEmitSchema]:
        emitted_events: List[SIOEmitSchema] = cls.SIO_EMIT_DATA + session_cls.SIO_EMIT_DATA # type: ignore
        return emitted_events


    def create_session(self, session_id: str) -> T:
        if session_id not in self.existing_sessions:
            session = self.session_cls(session_id, self.sio)
            self.existing_sessions[session_id] = session
            return session
        else:
            raise ValueError("Session already exists")
        
    async def trigger_event(self, event, sid, *args):
        handler_name = f"on_{event}"
        if not hasattr(self, handler_name):
            session = self.get_session_for_sid(sid)
            if handler_name in session.SIO_EVENT_HANDLERS:
                func = session.SIO_EVENT_HANDLERS[handler_name]
                if func is not None:
                    try:
                        return await func(session, sid, *args)
                    except Exception as e:
                        sys.stderr.write(f"{Fore.YELLOW}SIO SESSION ERROR: {event}{args}\nSee traceback:\n")
                        traceback.print_exc(file=sys.stderr)
                        raise e

            print(f"{Fore.YELLOW}SIO ERROR: {event} not found")
            return

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
    
    def init_api_routes(self):
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
        # print(f"Client {sid} connected.")
        pass

    async def on_disconnect(self, sid):
        # print(f"Client {sid} disconnected.")
        pass

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
    

async def test_setup(router_class: Type[SessionRouter] = SessionRouter):
    import uvicorn
    from fastapi import FastAPI
    import asyncio
    import socketio

    sio = socketio.AsyncServer(async_mode="asgi", namespaces=["/session"])
    app = FastAPI()
    app_asgi = socketio.ASGIApp(sio, app)

    config = uvicorn.Config(app_asgi, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)

    server_task = asyncio.create_task(server.serve())

    session_router = router_class(app, sio)
    session_name = "test-session"

    session_router.create_session(session_id=session_name)


    test_client = socketio.AsyncClient()
    test_client.on('connect', lambda: print("Connected to server"))

    await test_client.connect('http://localhost:8000', namespaces=["/session"])
    await test_client.emit('join_session', session_name, namespace="/session")

    return server, server_task, session_router, test_client


if __name__ == "__main__":
    import asyncio

    async def main():
        # SessionRouter.get_sio_handler_schema(Session)
        print(SessionRouter.get_emitted_events(Session))

    asyncio.run(main())