from __future__ import annotations
from datetime import datetime
from typing import List, NewType, Optional
from pydantic import BaseModel
from packages.server.web_architecture.sessionrouter import AbstractSession
from packages.tools.scribe import scribe_emits, scribe_handler
import asyncio
from packages.server.web_architecture.sessionrouter import Session

class MessageFromNPC(BaseModel):
    message: str
    timestamp: str
    npc_id: str

class ChatEvent(BaseModel):
    event: str
    timestamp: str
    npc_id: Optional[str] = None

class HumanMessage(BaseModel):
    message: str
    timestamp: str
    target_npc_id: Optional[str] = None

# class SessionMixin_Chat(Session):
#     @scribe_handler
#     async def on_chat_message(self, sid, data: HumanMessage) -> None:
#         print(f"Client {sid} sent message {data} in {self.session_id}")

#     @scribe_emits("chat_message", MessageFromNPC)
#     async def emit_chat_message(self, data: MessageFromNPC) -> None:
#         await self.emit("chat_message", data)

#     @scribe_emits("chat_event", ChatEvent)
#     async def emit_chat_event(self, data: ChatEvent) -> None:
#         await self.emit("chat_event", data)

