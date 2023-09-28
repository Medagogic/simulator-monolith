from typing import Dict, Optional
from fastapi import APIRouter
from pydantic import BaseModel
import socketio


class WebHandlerModuleBase(socketio.AsyncNamespace):
    def __init__(self, namespace: str, sio: socketio.AsyncServer, router: APIRouter):
        socketio.AsyncNamespace.__init__(self, namespace)
        sio.register_namespace(self)
        # self.router = router.

    async def on_connect(self, sid, environ):
        print(f"Client connected to socketio {self.namespace} with ID {sid}")

    async def on_disconnect(self, sid):
        print(f"Client disconnected from socketio {self.namespace} with ID {sid}")

    # def add_route(self, path: str, endpoint, methods: list[str]):
    #     full_path = f"/{path}"
    #     for method in methods:
    #         self.router.add_api_route(full_path, endpoint, methods=[method])


