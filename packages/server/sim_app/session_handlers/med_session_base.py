from __future__ import annotations
import socketio
from packages.medagogic_sim.main import MedagogicSimulator
from packages.server.web_architecture.sessionrouter import Session

from packages.medagogic_sim.logger.logger import get_logger, logging
logger = get_logger(level=logging.INFO)


class MedSessionBase(Session):
    def __init__(self, session_id: str, sio: socketio.AsyncServer):
        # For multiple inheritance
        if hasattr(self, '_init_done'):
            return
        else:
            self._init_done = True
    
        print(f"Initializing MedSessionBase with session_id {session_id}")
        Session.__init__(self, session_id=session_id, sio=sio)
        self.medsim = MedagogicSimulator()