
from fastapi import Depends
from packages.server.sim_app.med_sim.intervention_tracker import InterventionTracker
from packages.server.sim_app.med_sim.simulation4d import LeafyBlossom
from packages.server.sim_app.med_sim.simulation_time_keeper import DummyTimeKeeper
from packages.server.web_architecture.newsessionrouter import NewSessionRouter, Session


class SimSession(Session):
    def __init__(self, session_id: str):
        super().__init__(session_id)
        self.exercise_name = "Exercise 1"

        self.timekeeper = DummyTimeKeeper()
        self.intervention_tracker = InterventionTracker()
        self.sim = LeafyBlossom("packages/server/sim_app/med_sim/exercises/pediatric_septic_shock.txt",
                           timekeeper=self.timekeeper, 
                           intervention_tracker=self.intervention_tracker)


class SimSessionRouter(NewSessionRouter[SimSession]):
    def __init__(self, app):
        super().__init__(app, session_cls=SimSession)

    def init_routes(self):   
        @self.session_router.get("/medsim/vitals")
        async def medsim_vitals(session: SimSession = Depends(self.get_session)):
            return session.sim.getCurrentVitals()
        
        return super().init_routes()