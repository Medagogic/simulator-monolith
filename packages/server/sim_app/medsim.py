from __future__ import annotations
from datetime import datetime
from typing import List
from fastapi import Depends
from pydantic import BaseModel
import socketio
import packages.medagogic_sim.iomanager as iomanager
from packages.server.sim_app.chat import ChatEvent, HumanMessage, MessageFromNPC
from packages.medagogic_sim.main import MedagogicSimulator, VitalSigns
from packages.server.web_architecture.sessionrouter import Session, SessionRouter
from packages.tools.scribe import scribe_emits, scribe_handler
import asyncio


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



class Session_MedSim(Session):
    def __init__(self, session_id: str, sio: socketio.AsyncServer):
        super().__init__(session_id=session_id, sio=sio)

        self.medsim = MedagogicSimulator()

        self.medsim.context.iomanager.on_npc_speak.subscribe(self.handle_on_npc_speak)

        self.emit_vitals_loop()

    # CHAT
    def handle_on_npc_speak(self, data: iomanager.NPCSpeech) -> None:
        m = MessageFromNPC(
            message=data.text,
            timestamp=datetime.now().isoformat(),
            npc_id=data.npc_id,
        )
        asyncio.create_task(self.emit_chat_message(m))

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
    # END CHAT


    @scribe_emits("patient_vitals_update", VitalSigns)
    def emit_vitals_loop(self):
        if hasattr(self, "emit_vitals_loop_task"):
            return

        async def _loop() -> None:
            while True:
                vitals: VitalSigns = self.get_vitals()
                await self.emit("patient_vitals_update", vitals)
                await asyncio.sleep(1)

        task = asyncio.create_task(_loop())
        setattr(self, "emit_vitals_loop_task", task)
    

    def get_vitals(self) -> VitalSigns:
        return self.medsim.get_vitals()
    

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
        # await test_docs()
        print("\n")

        server, server_task, session_router, test_client = await setup_router_for_test(router_class=Router_MedSim)
        await asyncio.sleep(2) 

        # await test_client.emit('apply_interventions', InterventionData(interventions=["test1", "test2"]).model_dump(), namespace="/session")

        await asyncio.sleep(1)
        await test_client.disconnect()
        await server.shutdown()

    asyncio.run(run_test())