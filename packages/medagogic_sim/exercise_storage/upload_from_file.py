import argparse
import os
from pathlib import Path
from exercise_storage import ExerciseModel, ExerciseStorage

def upload_from_file(filename: str):
    this_dir = Path(os.path.dirname(os.path.realpath(__file__)))
    exercises_dir = Path(os.path.join(this_dir, Path('../_exercises')))
    metadata_file = exercises_dir / f"{filename}_metadata.txt"
    content_file = exercises_dir / f"{filename}.txt"
    
    if not metadata_file.exists() or not content_file.exists():
        print(f"Either {metadata_file} or {content_file} doesn't exist.")
        return

    with metadata_file.open('r') as f:
        exerciseMetadata = f.read().strip()

    with content_file.open('r') as f:
        exerciseData = f.read().strip()

    tags = ["development", "medagogic"]
    exercise = ExerciseModel(
        exerciseName=filename,
        exerciseData=exerciseData,
        exerciseMetadata=exerciseMetadata,
        tags=tags
    )

    storage = ExerciseStorage()
    storage.SaveExercise(exercise)
    print(f"Uploaded exercise: {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload exercise from file")
    parser.add_argument('filename', type=str, help="Name of the exercise file without extension")
    args = parser.parse_args()
    
    upload_from_file(args.filename)
