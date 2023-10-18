from __future__ import annotations
from datetime import datetime
from typing import List, NewType, Optional
from pydantic import BaseModel
from packages.server.web_architecture.sessionrouter import AbstractSession
from packages.tools.scribe import scribe_emits, scribe_handler
import asyncio

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

class SessionMixin_Chat(AbstractSession):
    test_loop: asyncio.Task

    @scribe_handler
    async def on_chat_message(self, sid, data: HumanMessage) -> None:
        print(f"Client {sid} sent message {data} in {self.session_id}")
        self.start_test_loop()

    @scribe_emits("chat_message", MessageFromNPC)
    async def emit_chat_message(self, data: MessageFromNPC) -> None:
        await self.emit("chat_message", data)

    @scribe_emits("chat_event", ChatEvent)
    async def emit_chat_event(self, data: ChatEvent) -> None:
        await self.emit("chat_event", data)

    def start_test_loop(self):
        if hasattr(self, "test_loop") and self.test_loop:
            if not self.test_loop.done():
                return

        async def test_loop():
            await self.emit_chat_message(MessageFromNPC(message="I'm preparing the medication now", timestamp=str(datetime.now()), npc_id="npc1"))
            await asyncio.sleep(3)
            await self.emit_chat_event(ChatEvent(event="perfoming chin lift", timestamp=str(datetime.now()), npc_id="npc1"))
    
        self.test_loop = asyncio.create_task(test_loop())