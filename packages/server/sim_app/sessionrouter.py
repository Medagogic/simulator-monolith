
from typing import List, Type
from fastapi import Depends
from pydantic import BaseModel
import socketio
from packages.server.web_architecture.sessionrouter import SessionRouter, Session, test_setup
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

class SimSessionRouter(SessionRouter[SimSession]):
    def __init__(self, app, sio: socketio.AsyncServer):
        super().__init__(app=app, sio=sio, session_cls=SimSession)

    def init_api_routes(self):   
        @self.session_router.get("/medsim/vitals")
        async def medsim_vitals(session: SimSession = Depends(self.get_session)):
            return session.medsim.get_vitals()
        
        return super().init_api_routes()
    
    @emits("test_event", SimUpdateData)
    def some_magic_function(self):
        self.emit("test_event", SimUpdateData(timestamp=0, value=0, name="test"))
    


if __name__ == "__main__":
    import asyncio
    import json

    async def main():
        server, server_task, session_router, test_client = await test_setup(router_class=SimSessionRouter)

        # cls: Type[Session] = session_router.session_cls
        # print(cls.SIO_EVENT_HANDLERS)

        SimSessionRouter.get_sio_handler_schema(SimSession)
        emits = SimSessionRouter.get_sio_emits_schema()
        print(json.dumps(emits, indent=4))

        # await test_client.emit("apply_interventions", {"interventions": ["medication"]}, namespace="/session")

        # session_router.create_session(session_id="session-2")
        # await test_client.emit("join_session", "session-2", namespace="/session")
        # await test_client.emit("apply_interventions", {"interventions": ["medication"]}, namespace="/session")

        # await asyncio.sleep(1) 

        await test_client.disconnect()
        await server.shutdown()


    asyncio.run(main())