
from fastapi import Depends
import socketio
from packages.server.web_architecture.sessionrouter import SessionRouter, Session
from packages.server.sim_app.med_sim._runner import MedsimRunner


class SimSession(Session):
    def __init__(self, session_id: str, sio: socketio.AsyncServer):
        super().__init__(session_id, sio)
        self.exercise_name = "Exercise 1"

        self.medsim = MedsimRunner(self.sio)

    def register_sio_events(self):
        @self.sio.event
        def test_event(sid, data):
            print(f"Test event received from {sid}: {data}")

        return super().register_sio_events()


class SimSessionRouter(SessionRouter[SimSession]):
    def __init__(self, app, sio: socketio.AsyncServer):
        super().__init__(app=app, sio=sio, session_cls=SimSession)

    def init_routes(self):   
        @self.session_router.get("/medsim/vitals")
        async def medsim_vitals(session: SimSession = Depends(self.get_session)):
            return session.medsim.get_vitals()
        
        return super().init_routes()
    
