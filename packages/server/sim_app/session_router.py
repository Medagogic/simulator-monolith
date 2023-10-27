from __future__ import annotations
from typing import List, Optional
from fastapi import Depends
from pydantic import BaseModel
import socketio
from packages.medagogic_sim.npc_definitions import NPCDefinition
from packages.medagogic_sim.main import VitalSigns
from packages.server.web_architecture.sessionrouter import SessionRouter
import asyncio
from packages.server.sim_app.session_handlers import *

from packages.medagogic_sim.logger.logger import get_logger, logging
from packages.tools.scribe.src.scribe import scribe_emits
logger = get_logger(level=logging.INFO)

class API_NPCData(BaseModel):
    id: str
    definition: NPCDefinition
    current_task: Optional[str] = None


class API_TeamData(BaseModel):
    npc_data: List[API_NPCData]

class SIO_TimeUpdate(BaseModel):
    exercise_time_seconds: int


class Session_MedSim(Session_Chat, Session_Patient, Session_DirectIntervention, Session_Devices):
    def __init__(self, session_id: str, sio: socketio.AsyncServer):
        Session_Chat.__init__(self, session_id=session_id, sio=sio)
        Session_Patient.__init__(self, session_id=session_id, sio=sio)
        Session_DirectIntervention.__init__(self, session_id=session_id, sio=sio)
        Session_Devices.__init__(self, session_id=session_id, sio=sio)

        self.time_loop()


    def api_get_team(self) -> API_TeamData:
        team_data = API_TeamData(npc_data=[])
        for id, npc in self.medsim.npc_manager.npcs.items():
            current_task = None
            if npc.actioner.current_task:
                current_task = npc.actioner.current_task.name
            npc_data = API_NPCData(
                id=id,
                definition=npc.definition,
                current_task=current_task
            )
            team_data.npc_data.append(npc_data)
        return team_data
    
    
    @scribe_emits("time_update", SIO_TimeUpdate)
    def time_loop(self):
        async def __loop():
            while True:
                await asyncio.sleep(1)
                data = SIO_TimeUpdate(exercise_time_seconds=self.medsim.context.simulation.timekeeper.exerciseTimeSeconds)
                await self.emit("time_update", data)
        asyncio.create_task(__loop())



class Router_MedSim(SessionRouter[Session_MedSim]):
    def __init__(self, app, sio: socketio.AsyncServer):
        super().__init__(app=app, sio=sio, session_cls=Session_MedSim)

    def init_api_routes(self):   
        @self.session_router.get("/medsim/vitals")
        async def medsim_vitals(session: Session_MedSim = Depends(self.get_session)):
            return session.medsim.get_exposed_vitals()
        
        @self.session_router.get("/medsim/team")
        async def medsim_team(session: Session_MedSim = Depends(self.get_session)) -> API_TeamData:
            return session.api_get_team()
        
        return super().init_api_routes()
    

if __name__ == "__main__":
    import asyncio
    from packages.server.web_architecture.sessionrouter import setup_router_for_test

    async def test_docs():
        for e in Router_MedSim.scribe_get_all_emitted_events(Session_MedSim):
            print(e)

        for h in Router_MedSim.scribe_get_all_handled_events(Session_MedSim):
            print(h)

    async def run_test():
        # await test_docs()
        print("\n")

        server, server_task, session_router, test_client = await setup_router_for_test(router_class=Router_MedSim)
        await asyncio.sleep(2) 

        # await test_client.emit('apply_interventions', InterventionData(interventions=["test1", "test2"]).model_dump(), namespace="/session")

        await asyncio.sleep(1)
        await test_client.disconnect()
        await server.shutdown()

    asyncio.run(test_docs())