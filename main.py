import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.responses import HTMLResponse
from web_architecture.session_manager import SessionManager
import socketio
import json
from sim_app.simulation_session import SimulationSessionHandler

class MainServer:
    def __init__(self):
        self.sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins='*')
        self.socket_app = socketio.ASGIApp(self.sio, socketio_path="/")

        routes = [
            APIRoute("/", endpoint=self.index, methods=["GET"])
        ]

        self.app = FastAPI(routes=routes)

        self.session_manager = SessionManager(sio=self.sio, app=self.app, session_type=SimulationSessionHandler)
        self.app.mount("/socket.io", self.socket_app)  # Here we mount socket app to main fastapi app

        self.__dump_api()

        # Define socket.io connection event handler
        @self.sio.on("connect")
        async def connect(sid, env):
            print("on connect")
            await self.sio.emit("response", {"content": "Hello world"}, room=sid)

        # Define socket.io message event handler
        @self.sio.on("message")
        async def broadcast(sid, msg):
            print(f"broadcast {msg}")
            await self.sio.emit("response", {"content": msg})  # or send to everyone


    async def index(self):
        return HTMLResponse(open("socket_test.html").read())

    def __dump_api(self):
        temp_session_id = "<session_id>"
        self.session_manager.create_session(session_id=temp_session_id)

        with open("openapi.json", "w") as file:
            json.dump(self.app.openapi(), file, indent=4)

        self.session_manager.destroy_session(temp_session_id)

server = MainServer()

def gunicorn():
    return server.app

if __name__ == "__main__":
    kwargs = {"host": "localhost", "port": 5000, "reload": True, "factory": True}
    uvicorn.run("main:gunicorn", **kwargs)
