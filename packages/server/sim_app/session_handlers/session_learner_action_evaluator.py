from __future__ import annotations
import asyncio
from typing import Optional
from packages.medagogic_sim.dr_clippy import DrClippyOutput
from packages.tools.scribe import scribe_emits
from .med_session_base import MedSessionBase
from packages.medagogic_sim.learner_actions.learner_action_evaluator import EvaluationChecklistItem, EvaluationChecklist

from packages.medagogic_sim.logger.logger import get_logger, logging
logger = get_logger(level=logging.INFO)


class Session_LearnerActionEvaluator(MedSessionBase):
    def __init__(self, session_id, sio):
        MedSessionBase.__init__(self, session_id=session_id, sio=sio)
        self.learner_action_evaluator = self.medsim.learner_action_evaluator
        self.learner_action_evaluator.on_learner_action_complete.subscribe(self.on_learner_action_complete)


    def on_learner_action_complete(self, item: EvaluationChecklistItem):
        asyncio.create_task(self.send_entire_checklist())
        
    
    async def send_full_state(self, sid: str):
        await self.send_entire_checklist(sid)


    @scribe_emits("learner_action_checklist", EvaluationChecklist)
    async def send_entire_checklist(self, sid: str=None):
        await self.emit("learner_action_checklist", self.learner_action_evaluator.checklist, to=sid)