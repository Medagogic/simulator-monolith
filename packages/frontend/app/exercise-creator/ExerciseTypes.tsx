export type VitalSigns = {
    temperature: string;
    heartRate: string;
    respiratoryRate: string;
    bloodPressure: string;
    bloodGlucose: string;
    oxygenSaturation: string;
    capillaryRefill: string;
};

export type ABCDE = {
    A: string;
    B: string;
    C: string;
    D: string;
    E: string;
};

export type GeneratedExerciseData = {
    patientName: string;
    patientAge: string;
    patientSex: string;
    patientHeight: string;
    patientWeight: string;
    backgroundInformation: string;
    simulationInstructions: string;
    initialVitalSigns: VitalSigns;
    initialABCDE: ABCDE;
    futureEvents: string;
    futureVitalSigns: VitalSigns;
    futureABCDE: ABCDE;
};

export const vitalSignsLabels: { [key in keyof VitalSigns]: string } = {
    temperature: "Temperature",
    heartRate: "Heart Rate",
    respiratoryRate: "Respiratory Rate",
    bloodPressure: "Blood Pressure",
    bloodGlucose: "Blood Glucose",
    oxygenSaturation: "Oxygen Saturation",
    capillaryRefill: "Capillary Refill",
};