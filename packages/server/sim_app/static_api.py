from typing import Dict, List, Union

from fastapi import Query
from packages.medagogic_sim.exercise_storage.exercise_storage import ExerciseModel, ExerciseStorage
from packages.server.web_architecture.static_api import StaticAPI
from packages.server.sim_app.exercise_creation.exercise_creator import ExerciseCreatorAPI
from packages.medagogic_sim.logger.logger import get_logger, logging

logger = get_logger(level=logging.INFO)

class MedagogicAPI(StaticAPI):
    def __init__(self):
        super().__init__()
        self.exercise_creator = ExerciseCreatorAPI(self.router)
        self.exercise_storage = ExerciseStorage()

        self.router.add_api_route("/exercises/list", self.search_exercises, methods=["GET"])
        self.router.add_api_route("/exercises/upload", self.upload_exercise, methods=["POST"])


    def search_exercises(self, name_filter: str = Query(""), tag_filter: List[str] = Query([])) -> List[ExerciseModel]:
        if len(name_filter.strip()) == 0:
            name_filter = None

        logger.info(f"Searching for exercises with tags: name_filter: {name_filter}, query: {tag_filter}")
        results = self.exercise_storage.ListExerciseModels(name_filter, tag_filter)
        logger.info(f"Found {len(results)} exercises")
        return results
    

    def upload_exercise(self, exercise: ExerciseModel) -> Dict:
        return self.exercise_storage.SaveExercise(exercise)