from __future__ import annotations
from datetime import datetime
from typing import List
from pydantic import BaseModel
from packages.server.web_architecture.sessionrouter import AbstractSession
from packages.server.web_architecture.scribe.scribe import scribe_emits, scribe_handler

class ChatMessage(BaseModel):
    message: str
    timestamp: datetime
    sender: str

class SessionMixin_Chat(AbstractSession):
    @scribe_handler
    async def on_chat_message(self, sid, data: str) -> None:
        print(f"Client {sid} sent message {data} in {self.session_id}")

    @scribe_emits("chat_message", ChatMessage)
    async def emit_chat_message(self, data: ChatMessage) -> None:
        await self.emit("chat_message", data)
