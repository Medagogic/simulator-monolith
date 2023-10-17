import pytest
from fastapi import FastAPI
import socketio
import asyncio
import uvicorn
from sessionrouter import SessionRouter, Session

# Constants for the test
TEST_SESSION_NAME = "test-session"
UNUSED_SESSION_NAME = "unused-sesh"


class SocketClientManager:
    def __init__(self):
        self.sio_client = socketio.AsyncClient()

    async def __aenter__(self):
        await self.sio_client.connect('http://localhost:8000', namespaces=['/session'])
        return self.sio_client  # This value is retrieved by the 'async with' statement

    async def __aexit__(self, exc_type, exc, tb):
        await self.sio_client.disconnect()
        await self.sio_client.wait()


AppSetup = tuple[FastAPI, SessionRouter, socketio.AsyncServer]
def app_components() -> AppSetup:
    sio = socketio.AsyncServer(async_mode="asgi", namespaces=["/session"])
    app = FastAPI()
    app_asgi = socketio.ASGIApp(sio, app)
    session_router = SessionRouter(app, sio, Session)

    return app_asgi, session_router, sio

class TestServer:
    __test__ = False

    def __init__(self):
        app_asgi, session_router, sio = app_components()

        self.app_asgi = app_asgi
        self.session_router = session_router
        self.sio = sio

        self.server_config = uvicorn.Config(app_asgi, host="localhost", port=8000, log_level="info")
        self.server = None  # We will initialize the actual server in the async context manager

    async def __aenter__(self):
        self.server = uvicorn.Server(config=self.server_config)
        self.server_task = asyncio.create_task(self.server.serve())
        while not self.server.started:
            await asyncio.sleep(0.01)  # This could potentially be a tighter loop than you want.
        return self.server

    async def __aexit__(self, exc_type, exc_value, traceback):
        self.server.should_exit = True
        await self.server_task
        self.server_task.cancel()
        await self.sio.eio.shutdown()
        await self.server_task
        await self.cleanup_background_tasks()

    async def cleanup_background_tasks(self):
        pending = asyncio.all_tasks()
        for task in pending:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass


@pytest.mark.asyncio
async def test_simple():
    print("Starting test")
    await asyncio.sleep(1)
    print("Done")


@pytest.mark.asyncio
async def test_socketio_connection() -> None:
    async with TestServer() as server:
        async with SocketClientManager() as socket_client:
            assert socket_client.sid is not None
            assert socket_client.connected is True


@pytest.mark.asyncio
async def test_sessions() -> None:
    async with TestServer() as server:
        async with SocketClientManager() as socket_client:
            await socket_client.emit('join_session', TEST_SESSION_NAME, namespace="/session")
            await socket_client.emit('test_event', {'example': 'data'}, namespace="/session")
