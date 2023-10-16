from packages.server.sim_app.med_sim.simulation4d import LeafyBlossom
from packages.server.sim_app.med_sim.simulation_types import VitalSigns
from packages.server.web_architecture.sessionhandler import SessionHandler_Base
from packages.server.web_architecture.webhandler import WebHandler_Base
from packages.server.sim_app.med_sim.simulation_time_keeper import DummyTimeKeeper
from packages.server.sim_app.med_sim.intervention_tracker import InterventionTracker

class MedsimWebHandler(WebHandler_Base):
    def __init__(self, sesh_handler: SessionHandler_Base):
        WebHandler_Base.__init__(self, namespace="medsim", sesh_handler=sesh_handler)

        timekeeper = DummyTimeKeeper()
        intervention_tracker = InterventionTracker()
        self.sim = LeafyBlossom("packages/server/sim_app/med_sim/exercises/pediatric_septic_shock.txt",
                           timekeeper=timekeeper, 
                           intervention_tracker=intervention_tracker)

        self.router.get("/vitals")(self.handle_get_vitals)
        self.router.get("/time")(self.handle_get_time)


    async def handle_get_vitals(self) -> VitalSigns:
        return self.sim.getCurrentVitals()
    

    async def handle_get_time(self) -> float:
        return self.sim.simulationTimeSeconds