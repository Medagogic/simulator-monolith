from pydantic import BaseModel

class PatientBasicInfo(BaseModel):
    age: str
    sex: str
    weight: str
    height: str

class ExerciseCreationParams(BaseModel):
    basic_info: PatientBasicInfo
    exerciseDescription: str
    simulationInstructions: str

class FullVitalSigns(BaseModel):
    temperature: str
    heartRate: str
    respiratoryRate: str
    bloodPressure: str
    bloodGlucose: str
    oxygenSaturation: str
    capillaryRefill: str

class FullABCDE(BaseModel):
    A: str
    B: str
    C: str
    D: str
    E: str

class FutureState(BaseModel):
    events: str
    vitalSigns: FullVitalSigns
    ABCDE: FullABCDE

class GeneratedExerciseData(BaseModel):
    patientName: str
    basicInfo: PatientBasicInfo
    simulationInstructions: str
    backgroundInformation: str
    vitalSigns: FullVitalSigns
    ABCDE: FullABCDE
    future: FutureState
