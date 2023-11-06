from typing import List, Optional, Union
import boto3
from mypy_boto3_dynamodb import ServiceResource
import os, dotenv
from packages.medagogic_sim.logger.logger import get_logger, logging
logger = get_logger(level=logging.INFO)

dotenv.load_dotenv()

from pydantic import BaseModel

class ExerciseModel(BaseModel):
    exerciseName: str
    exerciseData: str
    exerciseMetadata: str
    tags: List[str]


class ExerciseStorage:
    def __init__(self):
        self.dynamodb = self.init_dynamodb()
        self.table_name = "medagogic-exercises"
        self.table = self.dynamodb.Table(self.table_name)

    def init_dynamodb(self) -> ServiceResource:
        return boto3.resource("dynamodb", region_name='eu-north-1')

    def SaveExercise(self, exercise: ExerciseModel) -> dict:
        response = self.table.put_item(
            Item=exercise.model_dump()
        )
        return response

    def LoadExercise(self, exerciseName: str) -> Optional[ExerciseModel]:
        response = self.table.get_item(
            Key={
                'exerciseName': exerciseName
            }
        )
        item = response.get('Item')
        logger.info(f"Loaded exercise {exerciseName}")
        if item:
            return ExerciseModel(**item)
        else:
            return None

    def ListExerciseNames(self, search_tags: Optional[List[str]] = None) -> List[str]:
        response = self.table.scan()
        items = response.get('Items', [])
        
        if search_tags:
            items = [item for item in items if set(search_tags).issubset(set(item.get('tags', [])))]
        
        exercise_names = [item['exerciseName'] for item in items]
        return exercise_names
    

    def ListExerciseModels(self, name_filter: Optional[str] = None, tag_filter: Optional[List[str]] = None) -> List[ExerciseModel]:
        response = self.table.scan()
        items = response.get('Items', [])

        if name_filter and len(name_filter.strip()) > 0:
            items = [item for item in items if name_filter.lower() in item.get('exerciseName', "").lower()]
        
        if tag_filter and len(tag_filter) > 0:
            tag_filter = [tag.strip() for tag in tag_filter if tag.strip() != ""]
            items = [item for item in items if set(tag_filter).issubset(set(item.get('tags', [])))]

        return [ExerciseModel(**item) for item in items]



if __name__ == '__main__':
    import pytest
    import os

    module_dir = os.path.dirname(os.path.realpath(__file__))
    pytest.main(["-q", f"{module_dir}/test_exercise_storage.py"])
