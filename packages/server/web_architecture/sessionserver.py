from typing import Type
import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRoute
import socketio
import json
import asyncio
from fastapi.middleware.cors import CORSMiddleware
from web_architecture.static_api import StaticAPI
from packages.server.web_architecture.sessionrouter import NewSessionRouter


class SessionServer:
    def __init__(self, session_handler_class: Type[NewSessionRouter], static_api_class: StaticAPI = None):
        main_routes = [
            APIRoute("/save_docs", endpoint=self.save_api_json, methods=["POST"])
        ]

        self.app = FastAPI(routes=main_routes)  # type: ignore
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"]
        )

        self.sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
        self.socket_app = socketio.ASGIApp(self.sio, socketio_path="/")

        self.app.mount("/socket.io", self.socket_app)  # Here we mount socket app to main fastapi app

        self.static_api = static_api_class() if static_api_class else None
        self.app.include_router(self.static_api.router, prefix="/static_api") if self.static_api else None

        self.session_manager = session_handler_class(app=self.app, sio=self.sio)

        asyncio.create_task(self.save_api_json())

        # SocketIO test events
        # Define socket.io connection event handler
        @self.sio.on("connect")
        async def connect(sid, env):
            print(f"SIO client connection at / - {sid}")
            await self.sio.emit("response", {"content": "Hello world"}, room=sid)


    async def save_api_json(self):
        with open("openapi.json", "w") as file:
            json.dump(self.app.openapi(), file, indent=4)

        print("Saved API JSON")

        # sio_docs = {}
        # with open("socketio.json", "w") as file:
        #     for namespace, sio_handler in self.sio.namespace_handlers.items():
        #         if isinstance(sio_handler, WebHandler_Base):
        #             doc = type(sio_handler).generate_doc()
        #             sio_docs[namespace] = doc

        #     json.dump(sio_docs, file, indent=4)


def gunicorn():
    server = SessionServer(session_handler_class=NewSessionRouter)
    return server.app


if __name__ == "__main__":
    kwargs = {"host": "localhost", "port": 5000, "reload": True, "factory": True}
    uvicorn.run("main:gunicorn", **kwargs)  # type: ignore
