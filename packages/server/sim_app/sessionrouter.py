
from __future__ import annotations
from typing import List
from fastapi import Depends
from pydantic import BaseModel
import socketio
from packages.server.web_architecture.sessionrouter import SessionRouter, Session, test_setup, SessionRouterProtocol
from packages.server.sim_app.med_sim._runner import MedsimRunner
from packages.server.web_architecture.sio_api_emitters import emits

class InterventionData(BaseModel):
    interventions: List[str]

class SimSession(Session):
    def __init__(self, session_id: str, sio: socketio.AsyncServer):
        super().__init__(session_id, sio)
        self.exercise_name = "Exercise 1"

        self.medsim = MedsimRunner(self.sio)

    @Session.sio_handler
    async def on_apply_interventions(self, sid, data: InterventionData):
        print(f"Client {sid} applied interventions {data} in {self.session_id}")


class SimUpdateData(BaseModel):
    timestamp: float
    value: float
    name: str


class PatientStateMixin:
    @emits("patient_state", SimUpdateData)
    def emit_patient_state(self: SessionRouterProtocol, timestamp: float, value: float, name: str):
        self.emit("patient_state", SimUpdateData(timestamp=timestamp, value=value, name=name))


class SimSessionRouter(SessionRouter[SimSession], PatientStateMixin):
    def __init__(self, app, sio: socketio.AsyncServer):
        super().__init__(app=app, sio=sio, session_cls=SimSession)

    def init_api_routes(self):   
        @self.session_router.get("/medsim/vitals")
        async def medsim_vitals(session: SimSession = Depends(self.get_session)):
            return session.medsim.get_vitals()
        
        return super().init_api_routes()
    

if __name__ == "__main__":
    import asyncio
    import json

    async def main():
        server, server_task, session_router, test_client = await test_setup(router_class=SimSessionRouter)

        # cls: Type[Session] = session_router.session_cls
        # print(cls.SIO_EVENT_HANDLERS)

        print(SimSessionRouter.get_emitted_events(SimSession))

        # await test_client.emit("apply_interventions", {"interventions": ["medication"]}, namespace="/session")

        # session_router.create_session(session_id="session-2")
        # await test_client.emit("join_session", "session-2", namespace="/session")
        # await test_client.emit("apply_interventions", {"interventions": ["medication"]}, namespace="/session")

        # await asyncio.sleep(1) 

        await test_client.disconnect()
        await server.shutdown()


    asyncio.run(main())