from dataclasses import dataclass
import json
from typing import Any, Dict, Final, List, Optional
import markdown_to_json


from packages.medagogic_sim.exercise.simulation_types import ABCDE, BasicInfo, TimedValue, VitalSigns, Vitals, abcde_list_to_dict, parse_abcde_list, parse_vital_signs_list, parse_basic_info_list, vitals_list_to_dict


HEADER_EVENTS: Final = "Future Events"


def timed_vital_markdown(vitals_id: Vitals, timed_value: TimedValue) -> str:
    if vitals_id == Vitals.TEMPERATURE:
        return f"- Temperature: {timed_value.value:0.1f}°C @ {timed_value.time_str}"
    elif vitals_id == Vitals.HEART_RATE:
        return f"- Heart Rate: {timed_value.value:0.0f} bpm @ {timed_value.time_str}"
    elif vitals_id == Vitals.RESPIRATORY_RATE:
        return f"- Respiratory Rate: {timed_value.value:0.0f} breaths/min @ {timed_value.time_str}"
    elif vitals_id == Vitals.BLOOD_PRESSURE:
        return f"- Blood Pressure: {timed_value.value['systolic']:0.1f}/{timed_value.value['diastolic']:0.1f} mmHg @ {timed_value.time_str}"
    elif vitals_id == Vitals.BLOOD_GLUCOSE:
        return f"- Blood Glucose: {timed_value.value:0.0f} mg/dL @ {timed_value.time_str}"
    elif vitals_id == Vitals.OXYGEN_SATURATION:
        return f"- Oxygen Saturation: {timed_value.value:0.1f}% @ {timed_value.time_str}"
    elif vitals_id == Vitals.CAPILLARY_REFILL:
        return f"- Capillary Refill: {timed_value.value:0.0f} seconds @ {timed_value.time_str}"
    return f"Unknown vital sign: {vitals_id}"


@dataclass
class ProgressionDetails:
    events: List[str]
    vitals: Dict[Vitals, TimedValue]
    abcde: Dict[str, str]

    def to_markdown(self) -> str:
        markdown = ""

        markdown += f"## {HEADER_EVENTS}\n"
        for event in self.events:
            markdown += f"- {event}\n"

        markdown += "\n## Vital Signs\n"
        for vitals, timed_value in self.vitals.items():
            markdown += timed_vital_markdown(vitals, timed_value) + "\n"

        markdown += "\n## ABCDE\n"
        for abcde, description in self.abcde.items():
            markdown += f"- {abcde.upper()}: {description}\n"

        return markdown
    
    def update_vitals(self, vitals_dict: Dict[Vitals, TimedValue]) -> None:
        self.vitals.update(vitals_dict)

    def update_abcde(self, abcde_dict: Dict[str, str]) -> None:
        self.abcde.update(abcde_dict)


def _parse_state_progression(data_dict: Dict) -> ProgressionDetails:
    if "State Progression" not in data_dict:
        raise ValueError("State Progression not found in data_dict - old exercise format?")

    progression_dict = data_dict["State Progression"]
    events_list = progression_dict[HEADER_EVENTS]
    vitals_dict = vitals_list_to_dict(progression_dict["Vital Signs"])
    abcde_dict = abcde_list_to_dict(progression_dict["ABCDE"])
    
    progression_details = ProgressionDetails(events_list, vitals_dict, abcde_dict)

    return progression_details


def _markdown_dict_to_markdown_exercise(data_dict: Dict):
    patient_profile = data_dict["Patient Profile"]
    basic_info = parse_basic_info_list(patient_profile["Basic Information"])
    background_info = patient_profile["Background Information"]

    simulation_instructions = data_dict["Simulation Instructions"]

    current_vital_signs = parse_vital_signs_list(data_dict["Current Patient State"]["Vital Signs"])
    current_abcde = parse_abcde_list(data_dict["Current Patient State"]["ABCDE"])
    current_state = PatientState(current_vital_signs, current_abcde)

    progression = _parse_state_progression(data_dict)

    return MarkdownExercise(basic_info, background_info, simulation_instructions, current_state, progression)

    

class VitalSignsInterpolation:
    def __init__(self, vital_signs_at_0: VitalSigns, progression: ProgressionDetails):
        self.vital_signs_at_0 = vital_signs_at_0
        self.progression = progression
    
    def interpolate(self, minute: float) -> VitalSigns:
        """
        Interpolates the values of vital signs based on the given minute.
        """

        seconds = minute * 60
        
        interpolated_vitals: Dict[str, Any] = {}
        initial_vitals_dict = self.vital_signs_at_0.dict()
        for k, v in initial_vitals_dict.items():
            if k in self.progression.vitals:
                interpolated_vitals[k] = self.progression.vitals[k].interpolate(v, seconds)
            else:
                interpolated_vitals[k] = v

        return VitalSigns(**interpolated_vitals)



class PatientState:
    def __init__(self, vital_signs: VitalSigns, abcde: ABCDE, description: Optional[str]=None):
        self.vital_signs = vital_signs
        self.abcde = abcde
        self.description = description

    def to_markdown(self) -> str:
        markdown = ""

        if self.description is not None:
            markdown += f"## Description\n{self.description}\n\n"

        markdown += f"## Vital Signs\n{self.vital_signs.to_markdown()}\n\n## ABCDE\n{self.abcde.to_markdown()}"
        return markdown


class MarkdownExercise:
    def __init__(self, basic_info: BasicInfo, patient_background: str, simulation_instructions: List[str], current_state: PatientState, progression: ProgressionDetails):
        self.basic_info = basic_info
        self.patient_background = patient_background
        self.simulation_instructions = simulation_instructions
        self.current_state = current_state
        self.progression = progression

    @staticmethod
    def from_dict(data_dict: Dict)->"MarkdownExercise":
        return _markdown_dict_to_markdown_exercise(data_dict)
    
    @staticmethod
    def from_markdown(markdown: str)->"MarkdownExercise":
        data_dict = markdown_to_json.dictify(markdown)
        return _markdown_dict_to_markdown_exercise(data_dict)

    def to_markdown(self, include_progression=True):
        simulation_instructions = "\n".join([f"- {item}" for item in self.simulation_instructions])
        
        markdown = f"""
# Patient Profile
## Basic Information
{self.basic_info.to_markdown()}

## Background Information
{self.patient_background}

# Simulation Instructions
{simulation_instructions}

# Current Patient State
{self.current_state.to_markdown()}
"""

        if include_progression:
            markdown += f"""
# State Progression
{self.progression.to_markdown()}"""
        return markdown
    

if __name__ == "__main__":
    with open("autosim/simulation_services/v3_leafyblossom/exercises/pediatric_septic_shock.txt", "r") as f:
        exercise_definition = f.read()

    exercise = MarkdownExercise.from_markdown(exercise_definition)

    print(exercise.to_markdown())