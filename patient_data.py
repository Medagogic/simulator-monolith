# patient_data.py
from fastapi import APIRouter, FastAPI, HTTPException
from web_handler_module import WebHandlerModuleBase
import socketio

# router = APIRouter()

# class PatientData(BaseSessionModule):
#     def __init__(self, session_id: str):
#         super().__init__(session_id)
#         self.basic_info = {}

#     def set_basic_info(self, info: dict):
#         self.basic_info = info

#     def get_basic_info(self) -> dict:
#         return self.basic_info

# class PatientDataModuleManager(WebHandlerModuleBase):
#     def __init__(self, sio: socketio.AsyncServer):
#         super().__init__('/patient_data', sio)
#         self.add_route("/basic_info", self.get_patient_basic_info, ["GET"])

#     async def get_patient_basic_info(self, session_id: str):
#         return {"session_id": session_id}  # Implement as needed
    
#     async def on_connect(self, sid, environ):
#         print(f"Client connected to PatientDataModuleManager with session ID {sid}")

#     async def on_message(self, sid, data):
#         print(f"Recieved {data} from {sid}")
#         await self.emit("response", {"content": data}, room=sid)