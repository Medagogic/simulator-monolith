# from datetime import datetime
# from typing import Dict, Optional, Type
# from fastapi import APIRouter, FastAPI, Request
# from pydantic import BaseModel, Field
# import socketio
# import human_id
# from web_architecture.sessionhandler import SessionHandler_Base


# class SessionData(BaseModel):
#     session_id: str
#     sids_in_session: list[str]
#     creation_datetime: datetime = Field(default_factory=datetime.utcnow)



# class SessionManager():
#     def __init__(self, sio: socketio.AsyncServer, app: FastAPI, session_handler_class: Type[SessionHandler_Base]):
#         self.sio = sio
#         self.app = app
#         self.SessionHandlerClass = session_handler_class
#         self.sessionIdByUser: Dict[str, str] = {}
#         self.sessionDataBySessionId: Dict[str, SessionData] = {}
#         self.sessionsBySessionId: Dict[str, SessionHandler_Base] = {}

#         self.router = APIRouter(prefix="/session")
#         self.router.add_api_route("/new", self.handle_create_session, methods=["POST"])
#         self.router.add_api_route("/list", self.handle_list_sessions, methods=["GET"])

#         self.app.include_router(self.router)


#     async def handle_create_session(self):
#         session_id = self.create_session()
#         return session_id


#     async def handle_list_sessions(self) -> list[SessionData]:
#         return [d for d in self.sessionDataBySessionId.values()]
    

#     def create_session(self, sid: Optional[str]=None, session_id: str=None) -> str: # type: ignore
#         if not session_id:
#             session_id = human_id.generate_id()
#         session_data = SessionData(session_id=session_id, sids_in_session=[])
#         session = self.SessionHandlerClass(session_id, self.sio)

#         if sid:
#             self.sessionIdByUser[sid] = session_id
#             session_data.sids_in_session.append(sid)

#         self.sessionDataBySessionId[session_id] = session_data
#         self.sessionsBySessionId[session_id] = session

#         self.app.include_router(session.router, prefix=f"")
#         self.app.openapi_schema = None
#         self.app.setup()

#         return session_id
    

#     def destroy_session(self, session_id: str) -> None:
#         if not session_id in self.sessionDataBySessionId:
#             return
        
#         session = self.sessionsBySessionId[session_id]
#         for route in session.router.routes:
#             self.app.routes.remove(route)

#         self.app.openapi_schema = None
#         self.app.openapi()
#         self.app.setup()

#         del self.sessionDataBySessionId[session_id]
#         del self.sessionsBySessionId[session_id]


#     def remove_user_from_session(self, sid: str, delete_session_if_empty=True) -> None:
#         if sid not in self.sessionIdByUser:
#             return
        
#         session_id = self.sessionIdByUser[sid]
#         del self.sessionIdByUser[sid]

#         self.sessionDataBySessionId[session_id].sids_in_session.remove(sid)

#         if delete_session_if_empty:
#             if len(self.sessionDataBySessionId[session_id].sids_in_session) == 0:
#                 del self.sessionDataBySessionId[session_id]

