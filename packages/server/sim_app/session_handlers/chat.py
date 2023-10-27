from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
import socketio
import packages.medagogic_sim.iomanager as iomanager
from packages.server.sim_app.chat import ChatEvent, HumanMessage, MessageFromNPC
from packages.tools.scribe import scribe_emits, scribe_handler
import asyncio
from .med_session_base import MedSessionBase
from packages.medagogic_sim.npc_definitions import NPCDefinition

from packages.medagogic_sim.logger.logger import get_logger, logging
logger = get_logger(level=logging.INFO)


class SIO_NPCData(BaseModel):
    id: str
    definition: NPCDefinition
    current_task: Optional[str] = None


class ChatSession(MedSessionBase):
    def __init__(self, session_id: str, sio: socketio.AsyncServer):
        MedSessionBase.__init__(self, session_id=session_id, sio=sio)
        self.medsim.context.iomanager.on_npc_speak.subscribe(self.handle_on_npc_speak)
        self.medsim.context.iomanager.on_npc_start_action.subscribe(self.handle_on_npc_start_action)
        self.medsim.context.iomanager.on_npc_finished_action.subscribe(self.handle_on_npc_finished_action)

    def handle_on_npc_speak(self, data: iomanager.NPCSpeech) -> None:
        m = MessageFromNPC(
            message=data.text,
            timestamp=datetime.now().isoformat(),
            npc_id=data.npc_id,
        )
        asyncio.create_task(self.emit_chat_message(m))

    def handle_on_npc_start_action(self, data: iomanager.NPCAction) -> None:
        m = ChatEvent(
            event=f"{data.npc_name}: {data.task_info}",
            npc_id=data.npc_id,
            timestamp=datetime.now().isoformat(),
        )
        asyncio.create_task(self.emit_chat_event(m))

        npc = self.medsim.npc_manager.npcs[data.npc_id]
        npc_update_data = SIO_NPCData(
            id=npc.id,
            definition=npc.definition,
            current_task=data.task_info
        )
        asyncio.create_task(self.emit_npc_data(npc_update_data))

    def handle_on_npc_finished_action(self, data: iomanager.NPCAction) -> None:
        npc = self.medsim.npc_manager.npcs[data.npc_id]
        npc_update_data = SIO_NPCData(
            id=npc.id,
            definition=npc.definition,
            current_task=None
        )
        asyncio.create_task(self.emit_npc_data(npc_update_data))

    @scribe_handler
    async def on_chat_message(self, sid, data: HumanMessage) -> None:
        print(f"Client {sid} sent message {data} in {self.session_id}")
        await self.medsim.process_user_input(data["message"])

    @scribe_emits("chat_message", MessageFromNPC)
    async def emit_chat_message(self, data: MessageFromNPC) -> None:
        await self.emit("chat_message", data)

    @scribe_emits("chat_event", ChatEvent)
    async def emit_chat_event(self, data: ChatEvent) -> None:
        await self.emit("chat_event", data)
    
    @scribe_emits("npc_data", SIO_NPCData)
    async def emit_npc_data(self, data: SIO_NPCData) -> None:
        print(f"Sending NPC data: {data}")
        await self.emit("npc_data", data)
