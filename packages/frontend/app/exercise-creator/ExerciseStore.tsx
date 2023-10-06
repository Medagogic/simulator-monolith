import { GeneratedExerciseData } from "./ExerciseTypes";
import { create } from 'zustand';

type StoreState = {
    exerciseData: GeneratedExerciseData;
    setExerciseData: (data: GeneratedExerciseData) => void;
};

export const useExerciseStore = create<StoreState>((set) => ({
    exerciseData: {
        // make sure to provide initial values for all fields
        patientName: '',
        patientAge: '',
        patientSex: '',
        patientHeight: '',
        patientWeight: '',
        backgroundInformation: '',
        simulationInstructions: '',
        initialVitalSigns: {
            temperature: '',
            heartRate: '',
            respiratoryRate: '',
            bloodPressure: '',
            bloodGlucose: '',
            oxygenSaturation: '',
            capillaryRefill: '',
        },
        initialABCDE: {
            A: '',
            B: '',
            C: '',
            D: '',
            E: '',
        },
        futureEvents: '',
        futureVitalSigns: {
            temperature: '',
            heartRate: '',
            respiratoryRate: '',
            bloodPressure: '',
            bloodGlucose: '',
            oxygenSaturation: '',
            capillaryRefill: '',
        },
        futureABCDE: {
            A: '',
            B: '',
            C: '',
            D: '',
            E: '',
        },
    },
    setExerciseData: (data) => set((state) => ({
        exerciseData: {
            ...state.exerciseData,
            ...data
        }
    })),
}));
