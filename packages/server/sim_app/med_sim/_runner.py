from packages.server.sim_app.med_sim.simulation4d import LeafyBlossom
from packages.server.sim_app.med_sim.simulation_types import VitalSigns
from packages.server.sim_app.med_sim.simulation_time_keeper import DummyTimeKeeper
from packages.server.sim_app.med_sim.intervention_tracker import InterventionTracker

class MedsimRunner():
    def __init__(self):
        timekeeper = DummyTimeKeeper()
        intervention_tracker = InterventionTracker()
        self.sim = LeafyBlossom("packages/server/sim_app/med_sim/exercises/pediatric_septic_shock.txt",
                           timekeeper=timekeeper, 
                           intervention_tracker=intervention_tracker)


    async def get_vitals(self) -> VitalSigns:
        return self.sim.getCurrentVitals()
    

    async def get_time(self) -> float:
        return self.sim.simulationTimeSeconds