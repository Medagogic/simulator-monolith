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


