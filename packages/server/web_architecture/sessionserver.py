from typing import Type
from fastapi.responses import FileResponse
import uvicorn
from fastapi import FastAPI, Request
from fastapi.routing import APIRoute
import socketio
import json
import asyncio
from fastapi.middleware.cors import CORSMiddleware
from packages.server.lib.launch_config import LaunchConfig
from packages.server.web_architecture.static_api import StaticAPI
from packages.server.web_architecture.sessionrouter import SessionRouter
from fastapi.staticfiles import StaticFiles



class SessionServer:
    def __init__(self, session_handler_class: Type[SessionRouter], static_api_class: StaticAPI = None):
        main_routes = [
            
        ]

        self.app = FastAPI(routes=main_routes)  # type: ignore
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"]
        )

        self.sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=[]) # FastAPI handles CORS
        self.socket_app = socketio.ASGIApp(self.sio, socketio_path="/")

        self.app.mount("/socket.io", self.socket_app)  # Here we mount socket app to main fastapi app

        self.static_api = static_api_class() if static_api_class else None
        self.app.include_router(self.static_api.router, prefix="/static_api") if self.static_api else None

        self.session_manager = session_handler_class(app=self.app, sio=self.sio)

        # SocketIO test events
        # Define socket.io connection event handler
        @self.sio.on("connect")
        async def connect(sid, env):
            print(f"SIO client connection at / - {sid}")

        # This must be last, I think? Probably an indicator that something is fucked.
        self.__setup_serve_next_app()

    
    def __setup_serve_next_app(self) -> None:
        if LaunchConfig.noFrontend():
            print(f"Running with no frontend server")
            return
        
        self.app.mount("/_next/static", StaticFiles(directory="packages/frontend/out/_next/static"), name="static")

        def serve_index(full_path: Request):
            # Hacky as fuuuuck
            path = full_path.path_params['full_path']
            filenames = {
                "sim-session": "sim-session.html",
                "": "index.html",
            }
            if path in filenames:
                filename = filenames[path]
            else:
                filename = path
            return FileResponse(f"packages/frontend/out/{filename}")
        self.app.add_route("/{full_path:path}", serve_index, methods=["GET"])



def gunicorn():
    server = SessionServer(session_handler_class=SessionRouter)
    return server.app


if __name__ == "__main__":
    kwargs = {"host": "localhost", "port": 5000, "reload": True, "factory": True}
    uvicorn.run("main:gunicorn", **kwargs)  # type: ignore
