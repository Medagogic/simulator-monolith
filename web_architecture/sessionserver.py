from typing import Type
import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.responses import HTMLResponse
from web_architecture.sessionmanager import SessionManager
import socketio
import json
from web_architecture.sessionhandler import SessionHandler_Base
from web_architecture.webhandler import WebHandler_Base
import asyncio

class SessionServer:
    def __init__(self, session_handler_class: Type[SessionHandler_Base]):
        self.sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins='*')
        self.socket_app = socketio.ASGIApp(self.sio, socketio_path="/")

        main_routes = [
            APIRoute("/", endpoint=self.index, methods=["GET"]),
            APIRoute("/save_docs", endpoint=self.save_api_json, methods=["POST"])
        ]

        self.app = FastAPI(routes=main_routes)

        self.session_manager = SessionManager(sio=self.sio, app=self.app, session_handler_class=session_handler_class)
        self.app.mount("/socket.io", self.socket_app)  # Here we mount socket app to main fastapi app

        asyncio.create_task(self.save_api_json())

        # SocketIO test events
        # Define socket.io connection event handler
        @self.sio.on("connect")
        async def connect(sid, env):
            print(f"SIO client connection at / - {sid}")
            await self.sio.emit("response", {"content": "Hello world"}, room=sid)


    async def index(self):
        return HTMLResponse(open("socketio_test_page.html").read())
    

    async def save_api_json(self):
        print("Saving API JSON")
        temp_session_id = "<session_id>"
        self.session_manager.create_session(session_id=temp_session_id)

        with open("web_architecture/openapi.json", "w") as file:
            json.dump(self.app.openapi(), file, indent=4)

        sio_docs = {}
        with open("web_architecture/socketio.json", "w") as file:
            for namespace, sio_handler in self.sio.namespace_handlers.items():
                if isinstance(sio_handler, WebHandler_Base):
                    doc = type(sio_handler).generate_doc()
                    sio_docs[namespace] = doc

            json.dump(sio_docs, file, indent=4)

        self.session_manager.destroy_session(temp_session_id)


def gunicorn():
    server = SessionServer(session_handler_class=SessionHandler_Base)
    return server.app


if __name__ == "__main__":
    kwargs = {"host": "localhost", "port": 5000, "reload": True, "factory": True}
    uvicorn.run("main:gunicorn", **kwargs)
