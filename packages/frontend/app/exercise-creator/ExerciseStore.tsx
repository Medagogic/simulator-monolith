// import { GeneratedExerciseData } from "./ExerciseTypes";
import { GeneratedExerciseData } from '@/src/api';
import { create } from 'zustand';

type StoreState = {
    exerciseData: GeneratedExerciseData;
    setExerciseData: (data: GeneratedExerciseData) => void;
};

export const useExerciseStore = create<StoreState>((set) => ({
    exerciseData: {} as GeneratedExerciseData,
    setExerciseData: (data) => set((state) => ({
        exerciseData: {
            ...state.exerciseData,
            ...data
        }
    })),
}));
