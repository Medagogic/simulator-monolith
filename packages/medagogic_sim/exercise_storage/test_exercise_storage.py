import pytest
from moto import mock_dynamodb
import boto3
from exercise_storage import ExerciseModel, ExerciseStorage

@pytest.fixture
def dynamodb_fixture():
    with mock_dynamodb():
        dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
        dynamodb.create_table(
            TableName='medagogic-exercises',
            KeySchema=[{'AttributeName': 'exerciseName', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'exerciseName', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        yield

def test_save_and_load_exercise(dynamodb_fixture):
    storage = ExerciseStorage()
    exercise_to_save = ExerciseModel(
        exerciseName="exampleExercise",
        exerciseData="data_here",
        exerciseMetadata="metadata_here",
        tags=["tag1", "tag2"]
    )
    storage.SaveExercise(exercise_to_save)
    loaded_exercise = storage.LoadExercise("exampleExercise")

    assert loaded_exercise is not None
    assert loaded_exercise.exerciseName == "exampleExercise"
    assert loaded_exercise.exerciseData == "data_here"
    assert loaded_exercise.exerciseMetadata == "metadata_here"
    assert loaded_exercise.tags == ["tag1", "tag2"]


def test_list_exercises(dynamodb_fixture):
    storage = ExerciseStorage()

    exercise1 = ExerciseModel(
        exerciseName="exercise1",
        exerciseData="data1",
        exerciseMetadata="metadata1",
        tags=["tag1"]
    )
    storage.SaveExercise(exercise1)

    exercise2 = ExerciseModel(
        exerciseName="exercise2",
        exerciseData="data2",
        exerciseMetadata="metadata2",
        tags=["tag2"]
    )
    storage.SaveExercise(exercise2)

    all_exercises = storage.ListExerciseNames()
    assert set(all_exercises) == {"exercise1", "exercise2"}

    exercises_by_tag = storage.ListExerciseNames(search_tags=["tag1"])
    assert exercises_by_tag == ["exercise1"]


def test_load_exercise_not_found(dynamodb_fixture):
    storage = ExerciseStorage()
    loaded_exercise = storage.LoadExercise("nonExistentExercise")
    assert loaded_exercise is None
