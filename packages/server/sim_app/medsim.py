from __future__ import annotations
from typing import List
from fastapi import Depends
from pydantic import BaseModel
import socketio
from packages.server.sim_app.chat import SessionMixin_Chat
from packages.server.web_architecture.sessionrouter import Session, SessionRouter
from packages.server.web_architecture.scribe.scribe import scribe_emits, scribe_handler


class InterventionData(BaseModel):
    interventions: List[str]

class TestVitals(BaseModel):
    heart_rate: float
    blood_pressure: float
    temperature: float

class SimUpdateData(BaseModel):
    timestamp: float
    value: float
    name: str



class Session_MedSim(Session, SessionMixin_Chat):
    def get_vitals(self) -> TestVitals:
        return TestVitals(heart_rate=100, blood_pressure=120, temperature=38.6)
    
    @scribe_emits("patient_state", SimUpdateData)
    def emit_patient_state(self, timestamp: float, value: float, name: str):
        self.emit("patient_state", SimUpdateData(timestamp=timestamp, value=value, name=name))

    @scribe_handler
    async def on_apply_interventions(self, sid, data: InterventionData):
        print(f"Client {sid} applied interventions {data} in {self.session_id}")


class Router_MedSim(SessionRouter[Session_MedSim]):
    def __init__(self, app, sio: socketio.AsyncServer):
        super().__init__(app=app, sio=sio, session_cls=Session_MedSim)

    def init_api_routes(self):   
        @self.session_router.get("/medsim/vitals")
        async def medsim_vitals(session: Session_MedSim = Depends(self.get_session)):
            return session.get_vitals()
        
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
        await test_docs()
        print("\n")

        server, server_task, session_router, test_client = await setup_router_for_test(router_class=Router_MedSim)
        await asyncio.sleep(1) 

        await test_client.emit('apply_interventions', InterventionData(interventions=["test1", "test2"]).model_dump(), namespace="/session")

        await asyncio.sleep(1)
        await test_client.disconnect()
        await server.shutdown()


    asyncio.run(run_test())