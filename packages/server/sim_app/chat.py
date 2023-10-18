from __future__ import annotations
from typing import List
from pydantic import BaseModel
from packages.server.web_architecture.sessionrouter import SessionBase
from packages.server.web_architecture.scribe.scribe import scribe_emits, scribe_handler

class SessionMixin_Chat(SessionBase):
    @scribe_handler
    async def on_chat_message(self, sid, data: str) -> None:
        print(f"Client {sid} sent message {data} in {self.session_id}")


