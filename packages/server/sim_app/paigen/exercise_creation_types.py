from pydantic import BaseModel

class ExerciseCreationPatientBasicInfo(BaseModel):
    age: str
    sex: str
    weight: str
    height: str

class ExerciseCreationParams(BaseModel):
    basic_info: ExerciseCreationPatientBasicInfo
    exerciseDescription: str
    simulationInstructions: str

class ExerciseCreationVitalSigns(BaseModel):
    temperature: str
    heartRate: str
    respiratoryRate: str
    bloodPressure: str
    bloodGlucose: str
    oxygenSaturation: str
    capillaryRefill: str

class ExerciseCreationABCDE(BaseModel):
    A: str
    B: str
    C: str
    D: str
    E: str

class ExerciseCreationFutureState(BaseModel):
    events: str
    vitalSigns: ExerciseCreationVitalSigns
    ABCDE: ExerciseCreationABCDE

class GeneratedExerciseData(BaseModel):
    patientName: str
    basicInfo: ExerciseCreationPatientBasicInfo
    simulationInstructions: str
    backgroundInformation: str
    vitalSigns: ExerciseCreationVitalSigns
    ABCDE: ExerciseCreationABCDE
    future: ExerciseCreationFutureState
