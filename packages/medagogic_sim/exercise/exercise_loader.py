from typing import Final
from packages.medagogic_sim.exercise.metadata_loader import load_metadata, ExerciseMetadata

EXERCISE_PATH: Final[str] = "packages/medagogic_sim/_exercises"

def read_exercise(name: str) -> str:
    with open(f"{EXERCISE_PATH}/{name}.txt", "r") as f:
        return f.read()
    
def read_metadata(name: str) -> ExerciseMetadata:
    return load_metadata(EXERCISE_PATH, name)