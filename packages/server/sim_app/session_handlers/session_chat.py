from __future__ import annotations
from datetime import datetime
from typing import List, Optional, Union
from pydantic import BaseModel
import socketio
from packages.medagogic_sim.history.sim_history import Evt_Chat_Base, Evt_Chat_NPCMessage, Evt_Chat_Event, Evt_Chat_HumanMessage
import packages.medagogic_sim.iomanager as iomanager
from packages.tools.scribe import scribe_emits, scribe_handler
import asyncio
from packages.server.sim_app.session_handlers.med_session_base import MedSessionBase
from packages.medagogic_sim.npc_definitions import NPCDefinition

from packages.medagogic_sim.logger.logger import get_logger, logging
logger = get_logger(level=logging.INFO)



class SIO_NPCData(BaseModel):
    id: str
    definition: NPCDefinition
    current_task: Optional[str] = None


class SIO_ChatHistory(BaseModel):
    messages: List[Union[Evt_Chat_HumanMessage, Evt_Chat_Event, Evt_Chat_NPCMessage]]
    

class Session_Chat(MedSessionBase):
    def __init__(self, session_id: str, sio: socketio.AsyncServer):
        MedSessionBase.__init__(self, session_id=session_id, sio=sio)
        self.medsim.context.iomanager.on_npc_speak.subscribe(self.handle_on_npc_speak)
        self.medsim.context.iomanager.on_npc_start_action.subscribe(self.handle_on_npc_start_action)
        self.medsim.context.iomanager.on_npc_finished_action.subscribe(self.handle_on_npc_finished_action)
        self.medsim.context.iomanager.on_npc_thinking_updated.subscribe(self.handle_on_npc_thinking_updated)

    async def send_full_state(self, sid: str) -> None:
        for npc in self.medsim.npc_manager.npcs.values():
            npc_update_data = SIO_NPCData(
                id=npc.id,
                definition=npc.definition,
                current_task=None
            )
            asyncio.create_task(self.emit_npc_data(npc_update_data, to=sid))

        await self.send_full_chat_history(sid)


    @scribe_emits("full_chat_history", SIO_ChatHistory)
    async def send_full_chat_history(self, sid: str) -> None:
        chat_log = self.medsim.context.history.get_filtered_log(filter_types=[
            Evt_Chat_Base
        ])

        await self.emit("full_chat_history", SIO_ChatHistory(messages=chat_log), to=sid)


    @scribe_emits("npc_thinking_updated", iomanager.NPCThinking)
    def handle_on_npc_thinking_updated(self, data: iomanager.NPCThinking) -> None:
        asyncio.create_task(self.emit("npc_thinking_updated", data))

    def handle_on_npc_speak(self, data: iomanager.NPCSpeech) -> None:
        m = Evt_Chat_NPCMessage(
            content=data.text,
            timestamp=datetime.now().isoformat(),
            npc_id=data.npc_id,
        )
        asyncio.create_task(self.emit_chat_message(m))

    def handle_on_npc_start_action(self, data: iomanager.NPCAction) -> None:
        m = Evt_Chat_Event(
            content=f"{data.npc_name}: {data.task_info}",
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
    async def on_chat_message(self, sid, data: Evt_Chat_HumanMessage) -> None:
        print(f"Client {sid} sent message {data} in {self.session_id}")
        if "target_npc_id" not in data:
            data["target_npc_id"] = None
        await self.medsim.process_user_input(data["message"], data["target_npc_id"])

    @scribe_emits("chat_message", Evt_Chat_NPCMessage)
    async def emit_chat_message(self, data: Evt_Chat_NPCMessage) -> None:
        await self.emit("chat_message", data)

    @scribe_emits("chat_event", Evt_Chat_Event)
    async def emit_chat_event(self, data: Evt_Chat_Event) -> None:
        await self.emit("chat_event", data)
    
    @scribe_emits("npc_data", SIO_NPCData)
    async def emit_npc_data(self, data: SIO_NPCData, to=None) -> None:
        await self.emit("npc_data", data, to=to)
