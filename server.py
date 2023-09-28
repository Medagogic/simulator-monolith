# server.py
from typing import List
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse

from web_handler_module import WebHandlerModuleBase
from session_manager import SessionManager

import socketio

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins='*')
socket_app = socketio.ASGIApp(sio, socketio_path="/")
app = FastAPI()


@app.get("/test")
async def test():
    return HTMLResponse(open("socket_test.html").read())

session_manager = SessionManager(sio=sio, app=app)

app.mount("/socket.io", socket_app)  # Here we mount socket app to main fastapi app


@sio.on("connect")
async def connect(sid, env):
    print("on connect")
    await sio.emit("response", {"content": "Hello world"}, room=sid)

@sio.on("message")
async def broadcast(sid, msg):
    print(f"broadcast {msg}")
    await sio.emit("response", {"content": msg})  # or send to everyone


if __name__ == "__main__":
    kwargs = {"host": "localhost", "port": 5000, "reload": True}
    uvicorn.run("server:app", **kwargs)