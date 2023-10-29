from __future__ import annotations
import asyncio
from typing import Optional
from packages.medagogic_sim.dr_clippy import DrClippyOutput
from packages.tools.scribe import scribe_emits
from .med_session_base import MedSessionBase

from packages.medagogic_sim.logger.logger import get_logger, logging
logger = get_logger(level=logging.INFO)


class Session_DrClippy(MedSessionBase):
    def __init__(self, session_id, sio):
        MedSessionBase.__init__(self, session_id=session_id, sio=sio)
        logger.info("Session_DrClippy.__init__")
        self.dr_clippy = self.medsim.dr_clippy
        self.dr_clippy.on_new_advice.subscribe(self.handle_new_advice)

    @scribe_emits("dr_clippy_update", DrClippyOutput)
    async def emit_new_advice(self, drClippyOutput: DrClippyOutput, to: Optional[str]=None):
        logger.debug(f"Sending advice: {drClippyOutput}")
        await self.emit("dr_clippy_update", drClippyOutput, to=to)
    
    def handle_new_advice(self, advice: DrClippyOutput):
        asyncio.create_task(self.emit_new_advice(advice))
    
    async def send_full_state(self, sid: str):
        if self.dr_clippy.latest_advice is None:
            return
        await self.emit_new_advice(self.dr_clippy.latest_advice, to=sid)