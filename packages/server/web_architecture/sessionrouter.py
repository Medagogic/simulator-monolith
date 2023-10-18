from __future__ import annotations
from functools import wraps
import sys
import traceback
from fastapi import APIRouter, FastAPI, Depends, HTTPException
from typing import Any, Callable, Dict, Generic, List, Optional, Protocol, Type, TypeVar, Union
import human_id
from pydantic import BaseModel
import socketio
from packages.server.web_architecture.scribe.scribe import ScribeMixin_Handler, ScribeEmitSchema, ScribeMixin_Emit, ScribeHandlerSchema, scribe_emits, scribe_handler

from colorama import Fore
import colorama

colorama.init(autoreset=True)


from abc import ABC, abstractmethod, abstractproperty
SerializableType = Union[str, int, float, List[Any], Dict[str, Any]]
EmittableType = Union[SerializableType, BaseModel]

class AbstractSession(ABC):
    def __init__(self, session_id: str, sio: socketio.AsyncServer):
        pass

    @abstractproperty
    def session_id(self) -> str:
        pass

    @abstractproperty
    def sio(self) -> str:
        pass

    @abstractmethod
    async def emit(self, event_name: str, data: EmittableType) -> None:
        pass


class Session(AbstractSession, ScribeMixin_Emit, ScribeMixin_Handler):
    def __init__(self, session_id: str, sio: socketio.AsyncServer):
        self._session_id = session_id
        self._sio = sio

    @property
    def session_id(self) -> str:
        return self._session_id
    
    @property
    def sio(self) -> socketio.AsyncServer:
        return self._sio
    
    async def emit(self, event_name: str, data: EmittableType) -> None:
        if isinstance(data, BaseModel):
            data = data.model_dump()
        await self.sio.emit(event_name, data, room=self.session_id, namespace="/session")


# Use this protocol to type hint an object (mixins for the SessionRouter) which can emit events
class SessionRouterProtocol(Protocol):
    def emit(self, event_name: str, data: Any) -> None:
        ...


T = TypeVar('T', bound=Session)
class SessionRouter(socketio.AsyncNamespace, Generic[T], ScribeMixin_Emit, ScribeMixin_Handler):
    def __init__(self, app: FastAPI, sio: socketio.AsyncServer, session_cls: Type[T]=None) -> None: # type: ignore
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
    def scribe_get_all_handled_events(cls, session_cls: Type[ScribeMixin_Handler]):
        handled_events: List[ScribeHandlerSchema] = cls.scribe_get_handler_schema() + session_cls.scribe_get_handler_schema()
        return handled_events

    
    @classmethod
    def scribe_get_all_emitted_events(cls, session_cls: Type[ScribeMixin_Emit]) -> List[ScribeEmitSchema]:
        emitted_events: List[ScribeEmitSchema] = cls.scribe_get_emit_schema() + session_cls.scribe_get_emit_schema()
        return emitted_events


    def create_session(self, session_id: str) -> T:
        if session_id not in self.existing_sessions:
            session = self.session_cls(session_id, self.sio)
            self.existing_sessions[session_id] = session
            return session
        else:
            raise ValueError("Session already exists")
        
    @staticmethod
    async def __trigger_event_on_session(session: T, event: str, func: Callable, sid: str, *args) -> Any:
        try:
            return await func(session, sid, *args)
        except Exception as e:
            sys.stderr.write(f"{Fore.YELLOW}SIO SESSION ERROR: {event}{args}\nSee traceback:\n")
            traceback.print_exc(file=sys.stderr)
            raise e
        
    async def trigger_event(self, event: str, sid: str, *args) -> Any:
        if event.startswith("on_"):
            print(f"{Fore.RED}SCRIBE ERROR: Event name '{event}' cannot start with 'on_'")

        handler_name = f"on_{event}"
        if not hasattr(self, handler_name):
            session = self.get_session_for_sid(sid)
            func = session.scribe_get_handler(handler_name)
            if func is not None:
                return await self.__trigger_event_on_session(session, event, func, sid, *args)

            print(f"{Fore.YELLOW}SCRIBE ERROR: {event} not found")
        else:
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

    @scribe_handler
    async def on_join_session(self, sid, session_id: str):
        current_rooms = self.sio.rooms(sid, namespace=self.namespace)
        for room in current_rooms[1:]:
            print(f"Client {sid} left session {room}")
            self.sio.leave_room(sid, room, namespace=self.namespace)

        print(f"Client {sid} joined session {session_id}.")
        self.sio.enter_room(sid, session_id, namespace=self.namespace)

    @scribe_handler
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
    

async def setup_router_for_test(router_class: Type[SessionRouter] = SessionRouter):
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

    class TestSession(Session):
        @scribe_emits("test_event_from_session", str)
        def somefunc(self):
            pass

        @scribe_handler
        async def on_test_session(self, sid, data):
            print(f"Session: {sid}, {data}")

    class TestRouter(SessionRouter[TestSession]):
        def __init__(self, app, sio):
            super().__init__(app=app, sio=sio, session_cls=TestSession)

        @scribe_emits("test_event_from_router", float)
        def somefunc(self):
            pass

        @scribe_handler
        async def on_test_router(self, sid, data: str):
            print(f"Router: {data} from {sid}")

        @scribe_handler
        async def poop(self, sid, arse):
            print("hmm")

    async def test_scribe():
        for e in TestRouter.scribe_get_all_emitted_events(TestSession):
            print(e)

        for h in TestRouter.scribe_get_all_handled_events(TestSession):
            print(h)


    async def test_routing():
        await test_scribe()

        server, server_task, session_router, test_client = await setup_router_for_test(router_class=TestRouter)

        await asyncio.sleep(1) 

        await test_client.emit("test_router", "Hello, world!", namespace="/session")
        await test_client.emit("test_session", "Hello, world!", namespace="/session")

        await asyncio.sleep(1) 

        await test_client.disconnect()
        await server.shutdown()


    asyncio.run(test_routing())