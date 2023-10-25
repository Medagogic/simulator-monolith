# replace above with enum
from dataclasses import dataclass
from enum import Enum
import re
from typing import Any, Dict, Final, List, Optional, Union

from packages.medagogic_sim.logger.logger import get_logger, logging
logger = get_logger(level=logging.INFO)

from pydantic import BaseModel, Field
class Vitals(str, Enum):
    TEMPERATURE: Final = "temperature"
    HEART_RATE: Final = "heart_rate"
    RESPIRATORY_RATE: Final = "respiratory_rate"
    OXYGEN_SATURATION: Final = "oxygen_saturation"
    BLOOD_PRESSURE: Final = "blood_pressure"
    BLOOD_GLUCOSE: Final = "blood_glucose"
    CAPILLARY_REFILL: Final = "capillary_refill"
    SYSTOLIC: Final = "systolic"
    DIASTOLIC: Final = "diastolic"

class ActionType(str, Enum):
    NONE: Final = "none"
    ASSESSMENT: Final = "assessment"
    INTERVENTION: Final = "intervention"
    DEVICE: Final = "device"
    PREPARATION: Final = "preparation"
    OTHER: Final = "other"

class Basics:
    AGE: Final = "age"
    SEX: Final = "sex"
    WEIGHT: Final = "weight"
    HEIGHT: Final = "height"


class BloodPressureModel(BaseModel):
    systolic: float
    diastolic: float

    def vitals_dict(self) -> Dict[Vitals, float]:
        return {
            Vitals.SYSTOLIC: self.systolic,
            Vitals.DIASTOLIC: self.diastolic
        }

class VitalSigns(BaseModel):
    temperature: float = Field(..., description="The body temperature in degrees Celsius or Fahrenheit")
    heart_rate: float = Field(..., description="The heart rate in beats per minute")
    respiratory_rate: float = Field(..., description="The number of breaths taken per minute")
    blood_pressure: BloodPressureModel = Field(..., description="Blood pressure measurements")
    blood_glucose: float = Field(..., description="The blood glucose level")
    oxygen_saturation: float = Field(..., description="The oxygen saturation in percentage")
    capillary_refill: float = Field(..., description="The capillary refill time in seconds")
    
    class Config:
        json_schema_extra = {
            "example": {
                "temperature": 38.6,
                "heart_rate": 75,
                "respiratory_rate": 16,
                "blood_pressure": {
                    "systolic": 120,
                    "diastolic": 80
                },
                "blood_glucose": 5.5,
                "oxygen_saturation": 98,
                "capillary_refill": 2
            }
        }

    def __str__(self) -> str:
        return f"""===== VitalSigns
{self.to_markdown()}
===== End VitalSigns"""

    def to_markdown(self):
        markdown = [
            f"- Temperature: {self.temperature:0.1f}°C",
            f"- Heart Rate: {self.heart_rate:0.0f} bpm",
            f"- Respiratory Rate: {self.respiratory_rate:0.0f} breaths/min",
            f"- Blood Pressure: {self.blood_pressure.systolic:0.1f}/{self.blood_pressure.diastolic:0.1f} mmHg",
            f"- Blood Glucose: {self.blood_glucose:0.0f} mg/dL",
            f"- Oxygen Saturation: {self.oxygen_saturation:0.1f}%",
            f"- Capillary Refill: {self.capillary_refill:0.0f} seconds"
        ]
        return "\n".join(markdown)
    
    # def dict(self) -> Dict[Vitals, Any]:
    #     return {
    #         Vitals.TEMPERATURE: self.temperature,
    #         Vitals.HEART_RATE: self.heart_rate,
    #         Vitals.RESPIRATORY_RATE: self.respiratory_rate,
    #         Vitals.BLOOD_PRESSURE: self.blood_pressure,
    #         Vitals.OXYGEN_SATURATION: self.oxygen_saturation,
    #         Vitals.BLOOD_GLUCOSE: self.blood_glucose,
    #         Vitals.CAPILLARY_REFILL: self.capillary_refill
    #     }
    
    def update_from_dict(self, vitals_dict: Dict[Vitals, Any]) -> None:
        if Vitals.TEMPERATURE in vitals_dict:
            self.temperature = vitals_dict[Vitals.TEMPERATURE]
        if Vitals.HEART_RATE in vitals_dict:
            self.heart_rate = vitals_dict[Vitals.HEART_RATE]
        if Vitals.RESPIRATORY_RATE in vitals_dict:
            self.respiratory_rate = vitals_dict[Vitals.RESPIRATORY_RATE]
        if Vitals.BLOOD_PRESSURE in vitals_dict:
            self.blood_pressure = vitals_dict[Vitals.BLOOD_PRESSURE]
        if Vitals.OXYGEN_SATURATION in vitals_dict:
            self.oxygen_saturation = vitals_dict[Vitals.OXYGEN_SATURATION]
        if Vitals.BLOOD_GLUCOSE in vitals_dict:
            self.blood_glucose = vitals_dict[Vitals.BLOOD_GLUCOSE]
        if Vitals.CAPILLARY_REFILL in vitals_dict:
            self.capillary_refill = vitals_dict[Vitals.CAPILLARY_REFILL]
    
class BasicInfo:
    def __init__(self, age: str, sex: str, weight: str, height: str):
        self.age = age
        self.sex = sex
        self.weight = weight
        self.height = height

    def __str__(self) -> str:
        return f"""===== BasicInfo
{self.to_markdown()}
===== End BasicInfo"""

    def to_markdown(self) -> str:
        markdown = [
            f"- Age: {self.age}",
            f"- Sex: {self.sex}",
            f"- Weight: {self.weight}",
            f"- Height: {self.height}"
        ]
        return "\n".join(markdown)
    
    def dict(self) -> Dict:
        return {
            Basics.AGE: self.age,
            Basics.SEX: self.sex,
            Basics.WEIGHT: self.weight,
            Basics.HEIGHT: self.height
        }


def vitals_dict_to_markdown(vitals: Dict[Vitals, Any]):
    markdown = []
    
    if Vitals.TEMPERATURE in vitals:
        markdown.append(f"- Temperature: {vitals[Vitals.TEMPERATURE]:0.1f}°C")
    if Vitals.HEART_RATE in vitals:
        markdown.append(f"- Heart Rate: {vitals[Vitals.HEART_RATE]:0.0f} bpm")
    if Vitals.RESPIRATORY_RATE in vitals:
        markdown.append(f"- Respiratory Rate: {vitals[Vitals.RESPIRATORY_RATE]:0.0f} breaths/min")
    if Vitals.BLOOD_PRESSURE in vitals:
        markdown.append(f"- Blood Pressure: {vitals[Vitals.BLOOD_PRESSURE][Vitals.SYSTOLIC]:0.1f}/{vitals[Vitals.BLOOD_PRESSURE][Vitals.DIASTOLIC]:0.1f} mmHg")
    if Vitals.BLOOD_GLUCOSE in vitals:
        markdown.append(f"- Blood Glucose: {vitals[Vitals.BLOOD_GLUCOSE]:0.0f} mg/dL")
    if Vitals.OXYGEN_SATURATION in vitals:
        markdown.append(f"- Oxygen Saturation: {vitals[Vitals.OXYGEN_SATURATION]:0.1f}%")
    if Vitals.CAPILLARY_REFILL in vitals:
        markdown.append(f"- Capillary Refill: {vitals[Vitals.CAPILLARY_REFILL]:0.0f} seconds")

    return "\n".join(markdown)


def basic_info_dict_to_markdown(basic_info: Dict[str, Any]) -> str:
    markdown = []
    
    if Basics.AGE in basic_info:
        markdown.append(f"- Age: {basic_info[Basics.AGE]}")
    if Basics.SEX in basic_info:
        markdown.append(f"- Sex: {basic_info[Basics.SEX]}")
    if Basics.WEIGHT in basic_info:
        markdown.append(f"- Weight: {basic_info[Basics.WEIGHT]}")
    if Basics.HEIGHT in basic_info:
        markdown.append(f"- Height: {basic_info[Basics.HEIGHT]}")

    return "\n".join(markdown)

    
class ABCDE:
    def __init__(self, a: str, b: str, c: str, d: str, e: str):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e

    def update_from_dict(self, abcde_dict: Dict[str, str]) -> None:
        if "a" in abcde_dict:
            self.a = abcde_dict["a"]
        if "b" in abcde_dict:
            self.b = abcde_dict["b"]
        if "c" in abcde_dict:
            self.c = abcde_dict["c"]
        if "d" in abcde_dict:
            self.d = abcde_dict["d"]
        if "e" in abcde_dict:
            self.e = abcde_dict["e"]

    def to_markdown(self):
        return "\n".join([
            f"- A: {self.a}",
            f"- B: {self.b}",
            f"- C: {self.c}",
            f"- D: {self.d}",
            f"- E: {self.e}"
        ])
    
    def to_dict(self):
        return {
            "a": self.a,
            "b": self.b,
            "c": self.c,
            "d": self.d,
            "e": self.e
        }
    

def parse_basic_info_list(basic_info_list: List[str]) -> "BasicInfo":
    basic_info: Dict[str, Any] = {}
    for item in basic_info_list:
        if "Age" in item:
            basic_info[Basics.AGE] = item.replace("Age: ", "").strip()
        elif "Sex" in item:
            basic_info[Basics.SEX] = item.replace("Sex: ", "").strip()
        elif "Weight" in item:
            basic_info[Basics.WEIGHT] = item.replace("Weight: ", "").strip()
        elif "Height" in item:
            basic_info[Basics.HEIGHT] = item.replace("Height: ", "").strip()
    return BasicInfo(**basic_info)  # type: ignore
    

def interpolate_values(value0: Union[float, BloodPressureModel], value1: Union[float, dict], t: float) -> Union[float, dict]:
    if type(value0) == type(float) and type(value1) != type(float):
        raise TypeError("value0 and value1 must be the same type")
    elif isinstance(value0, BloodPressureModel) and not isinstance(value1, dict):
        raise TypeError("value0 and value1 must be compatible types")
    
    if isinstance(value0, BloodPressureModel):
        value0 = value0.vitals_dict()   # type: ignore

    if isinstance(value0, float):
        return value0 * (1 - t) + value1 * t    # type: ignore
    elif isinstance(value0, dict):
        if set(value0.keys()) != set(value1.keys()):    # type: ignore
            raise ValueError("value0 and value1 must have the same keys")

        interpolated_dict = {}
        for key in value0:
            interpolated_dict[key] = value0[key] * (1 - t) + value1[key] * t    # type: ignore
        return interpolated_dict
    else:
        raise TypeError(f"Unexpected type {type(value0).__name__} for interpolation")



@dataclass
class TimedValue:
    time_str: Optional[str]
    value: Any

    @property
    def time_seconds(self) -> int:
        if not self.time_str:
            return 0
        if "minutes" in self.time_str:
            return int(self.time_str.replace("minutes", "").strip()) * 60
        elif "minute" in self.time_str:
            return int(self.time_str.replace("minute", "").strip()) * 60
        elif "seconds" in self.time_str:
            return int(self.time_str.replace("seconds", "").strip())
        elif "second" in self.time_str:
            return int(self.time_str.replace("second", "").strip())
        raise ValueError(f"Unexpected time string {self.time_str}")
    
    def interpolate(self, value0: Any, interpolation_time_seconds: float) -> Any:
        if self.time_seconds <= 0:
            return value0
        if interpolation_time_seconds >= self.time_seconds:
            return self.value
        
        t = interpolation_time_seconds / self.time_seconds
        return interpolate_values(value0, self.value, t)
    

def vitals_list_to_dict(vitals_list: List[str]) -> Dict[Vitals, TimedValue]:
    try:
        vital_signs: Dict[Vitals, TimedValue] = {}
        for item in vitals_list:
            if "no change" in item.lower():
                continue

            if "@" in item:
                item_details, time = item.split("@")
                item_details = item_details.strip()
                time = time.strip()
            else:
                item_details = item
                time = None

            if "Temperature" in item_details:
                value = float(item_details.replace("Temperature: ", "").replace("°C", "").strip())
                vital_signs[Vitals.TEMPERATURE] = TimedValue(time, value)
            elif "Heart Rate" in item_details:
                value = float(re.findall(r'\d+', item_details)[0])
                vital_signs[Vitals.HEART_RATE] = TimedValue(time, value)
            elif "Respiratory Rate" in item_details:
                value = float(re.findall(r'\d+', item_details)[0])
                vital_signs[Vitals.RESPIRATORY_RATE] = TimedValue(time, value)
            elif "Blood Pressure" in item_details:
                bp = item_details.replace("Blood Pressure: ", "").replace("mmHg", "").strip().split("/")
                value = {Vitals.SYSTOLIC: float(bp[0]), Vitals.DIASTOLIC: float(bp[1])}   # type: ignore
                vital_signs[Vitals.BLOOD_PRESSURE] = TimedValue(time, value)
            elif "Oxygen Saturation" in item_details:
                value = float(re.findall(r'\d+', item_details)[0])
                vital_signs[Vitals.OXYGEN_SATURATION] = TimedValue(time, value)
            elif "Blood Glucose" in item_details:
                value = float(re.findall(r'\d+', item_details)[0])
                vital_signs[Vitals.BLOOD_GLUCOSE] = TimedValue(time, value)
            elif "Capillary Refill" in item_details:
                value = float(re.findall(r'\d+', item_details)[0])
                vital_signs[Vitals.CAPILLARY_REFILL] = TimedValue(time, value)
        return vital_signs
    except Exception as e:
        logger.error(f"Error parsing vitals list {vitals_list}")
        logger.error(vitals_list)
        raise e



def parse_vital_signs_list(vital_signs_list: List[str]) -> "VitalSigns":
    parsed_vitals = vitals_list_to_dict(vital_signs_list)
    for vital, timed_value in parsed_vitals.items():
        parsed_vitals[vital] = timed_value.value
    return VitalSigns(**parsed_vitals)    # type: ignore


def abcde_list_to_dict(abcde_list: List[str]) -> Dict[str, str]:
    abcde = {}
    for item in abcde_list:
        if item.startswith("A:"):
            abcde["a"] = item[3:]
        elif item.startswith("B:"):
            abcde["b"] = item[3:]
        elif item.startswith("C:"):
            abcde["c"] = item[3:]
        elif item.startswith("D:"):
            abcde["d"] = item[3:]
        elif item.startswith("E:"):
            abcde["e"] = item[3:]
    return abcde

def parse_abcde_list(abcde_list: List[str]) -> "ABCDE":
    return ABCDE(**abcde_list_to_dict(abcde_list))
