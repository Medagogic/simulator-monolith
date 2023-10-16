
from fastapi import Depends
import socketio
from packages.server.sim_app.med_sim.intervention_tracker import InterventionTracker
from packages.server.sim_app.med_sim.simulation4d import LeafyBlossom
from packages.server.sim_app.med_sim.simulation_time_keeper import DummyTimeKeeper
from packages.server.web_architecture.sessionrouter import NewSessionRouter, Session
from packages.server.sim_app.med_sim._runner import MedsimRunner


class SimSession(Session):
    def __init__(self, session_id: str, sio: socketio.AsyncServer):
        super().__init__(session_id, sio)
        self.exercise_name = "Exercise 1"

        self.medsim = MedsimRunner()


class SimSessionRouter(NewSessionRouter[SimSession]):
    def __init__(self, app, sio: socketio.AsyncServer):
        super().__init__(app=app, sio=sio, session_cls=SimSession)

    def init_routes(self):   
        @self.session_router.get("/medsim/vitals")
        async def medsim_vitals(session: SimSession = Depends(self.get_session)):
            return session.medsim.get_vitals()
        
        return super().init_routes()