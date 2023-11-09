from dataclasses import dataclass, field
import os
from typing import List
import markdown_to_json


@dataclass
class ExerciseMetadata:
    case_description: str = "Missing metadata file"
    vignette: str = "Missing metadata file"
    case_summary: str = "Missing metadata file"
    expected_actions: List[str] = field(default_factory=list) 

    @staticmethod
    def from_markdown_str(markdown: str) -> "ExerciseMetadata":
        metadata = markdown_to_json.dictify(markdown)

        return ExerciseMetadata(
            case_description=metadata["Case Description"],
            vignette=metadata["Vignette"],
            case_summary=metadata["Case Summary"],
            expected_actions=metadata["Expected Actions"]
        )


def load_metadata(path: str, exercise_name: str):
    file_path = os.path.join(path, f"{exercise_name}_metadata.txt")

    if not os.path.exists(file_path):
        return ExerciseMetadata()

    with open(file_path, "r") as f:
        contents = f.read()

    return ExerciseMetadata.from_markdown_str(contents)


if __name__ == "__main__":
    metadata = load_metadata("pediatric_septic_shock")
    print(metadata.case_description)