from __future__ import annotations
from datetime import datetime
from typing import Dict, List, Optional
from fastapi import Depends
from pydantic import BaseModel
import socketio
from packages.medagogic_sim.exercise.markdownexercise import MarkdownExercise
from packages.medagogic_sim.exercise.simulation_types import ActionType
from packages.medagogic_sim.history.sim_history import Evt_Assessment, Evt_CompletedIntervention, Evt_StartTask, Evt_TaskConsequence, HistoryEvent
import packages.medagogic_sim.iomanager as iomanager
from packages.medagogic_sim.npc_definitions import NPCDefinition
from packages.server.sim_app.chat import ChatEvent, HumanMessage, MessageFromNPC
from packages.medagogic_sim.main import MedagogicSimulator, VitalSigns
from packages.server.web_architecture.sessionrouter import Session, SessionRouter
from packages.tools.scribe import scribe_emits, scribe_handler
import asyncio
from .med_session_base import MedSessionBase

from packages.medagogic_sim.logger.logger import get_logger, logging
logger = get_logger(level=logging.INFO)


class CombatLogElement(BaseModel):
    timestamp: float
    npc_name: str
    content: str

class CombatLogUpdateData(BaseModel):
    log: List[CombatLogElement]



class Session_Patient(MedSessionBase):
    def __init__(self, session_id: str, sio: socketio.AsyncServer):
        MedSessionBase.__init__(self, session_id=session_id, sio=sio)
        self.medsim.context.history.on_new_event.subscribe(self.handle_on_new_history_event)
        self.emit_vitals_loop()


    @scribe_emits("combatlog_update", CombatLogUpdateData)
    def handle_on_new_history_event(self, event: HistoryEvent) -> None:
        full_combat_log = self.medsim.context.history.get_filtered_log(filter_types=[
            Evt_Assessment,
            Evt_StartTask,
            Evt_TaskConsequence,
            Evt_CompletedIntervention
        ])

        data = CombatLogUpdateData(
            log = [CombatLogElement(
                timestamp=e.timestamp,
                npc_name=e.npc_name,
                content=e.content
            ) for e in full_combat_log]
        )
        asyncio.create_task(self.emit("combatlog_update", data))


    @scribe_emits("patient_vitals_update", VitalSigns)
    def emit_vitals_loop(self):
        if hasattr(self, "emit_vitals_loop_task"):
            return

        async def _loop() -> None:
            while True:
                vitals: VitalSigns = self.api_get_vitals()
                await self.emit("patient_vitals_update", vitals)
                await asyncio.sleep(1)

        task = asyncio.create_task(_loop())
        setattr(self, "emit_vitals_loop_task", task)
      