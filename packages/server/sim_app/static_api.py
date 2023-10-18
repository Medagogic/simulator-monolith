from packages.server.web_architecture.static_api import StaticAPI
from packages.server.sim_app.exercise_creation.exercise_creator import ExerciseCreatorAPI

class MedagogicAPI(StaticAPI):
    def __init__(self):
        super().__init__()
        self.exercise_creator = ExerciseCreatorAPI(self.router)