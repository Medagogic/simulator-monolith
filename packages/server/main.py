import uvicorn
from sim_app.simulation_session import SimulationSessionHandler
from sim_app.static_api import MedagogicAPI
from web_architecture.sessionserver import SessionServer


def gunicorn():
    server = SessionServer(session_handler_class=SimulationSessionHandler, static_api_class=MedagogicAPI)
    return server.app


if __name__ == "__main__":
    kwargs = {"host": "localhost", "port": 5000, "reload": True, "factory": True}
    uvicorn.run("main:gunicorn", **kwargs)
