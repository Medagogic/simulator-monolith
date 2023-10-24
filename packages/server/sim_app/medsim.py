from __future__ import annotations
from datetime import datetime
from typing import List
from fastapi import Depends
from pydantic import BaseModel
import socketio
from packages.medagogic_sim.exercise.markdownexercise import MarkdownExercise
from packages.medagogic_sim.exercise.simulation_types import ActionType
from packages.medagogic_sim.history.sim_history import Evt_Assessment, Evt_CompletedIntervention, Evt_StartTask, Evt_TaskConsequence, HistoryEvent
import packages.medagogic_sim.iomanager as iomanager
from packages.server.sim_app.chat import ChatEvent, HumanMessage, MessageFromNPC
from packages.medagogic_sim.main import MedagogicSimulator, VitalSigns
from packages.server.web_architecture.sessionrouter import Session, SessionRouter
from packages.tools.scribe import scribe_emits, scribe_handler
import asyncio

from packages.medagogic_sim.logger.logger import get_logger, logging
logger = get_logger(level=logging.INFO)

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

class CombatLogElement(BaseModel):
    timestamp: float
    npc_name: str
    content: str

class CombatLogUpdateData(BaseModel):
    log: List[CombatLogElement]


class Session_MedSim(Session):
    def __init__(self, session_id: str, sio: socketio.AsyncServer):
        super().__init__(session_id=session_id, sio=sio)

        self.medsim = MedagogicSimulator()

        self.medsim.context.iomanager.on_npc_speak.subscribe(self.handle_on_npc_speak)
        self.medsim.context.iomanager.on_npc_action.subscribe(self.handle_on_npc_action)
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

    # CHAT
    def handle_on_npc_speak(self, data: iomanager.NPCSpeech) -> None:
        m = MessageFromNPC(
            message=data.text,
            timestamp=datetime.now().isoformat(),
            npc_id=data.npc_id,
        )
        asyncio.create_task(self.emit_chat_message(m))

    def handle_on_npc_action(self, data: iomanager.NPCAction) -> None:
        m = ChatEvent(
            event=f"{data.npc_name}: {data.task_info}",
            npc_id=data.npc_id,
            timestamp=datetime.now().isoformat(),
        )
        asyncio.create_task(self.emit_chat_event(m))

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

    @scribe_handler
    async def on_direct_intervention(self, sid, function_call: str) -> None:
        print(f"Client {sid} called on_direct_intervention `{function_call}` in {self.session_id}")
        task = self.medsim.context.action_db.get_action_from_call(function_call, function_call)
        if task.type == "intervention":
            params_str = ", ".join(task.call_data.params)
            receipt = self.medsim.context.simulation.applyUpdate(f"Dr Whoopie performed action: `{task.call_data.name} ({params_str})`")

            receipt.on_new_immediate_state_generated.subscribe(self.direct_intervention_current_state_recalculated)
            receipt.on_finished.subscribe(self.direct_intervention_finished)
        else:
            raise Exception(f"Task {task} is not an intervention")
    
    def direct_intervention_current_state_recalculated(self, data):
        exercise, comments = data
        logger.info(f"Current state recalculated: {exercise}")
        logger.info(f"Comments: {comments}")

    def direct_intervention_finished(self, null):
        exercise = self.medsim.context.simulation.exercise
        logger.info(f"Finished direct intervention: {exercise}")

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