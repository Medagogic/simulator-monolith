
import { create } from "zustand";

type SessionStore = {
    exerciseTimeSeconds: number;
    setExerciseTimeSeconds: (exerciseTimeSeconds: number) => void;
};

export const useSessionStore = create<SessionStore>((set, get) => ({
    exerciseTimeSeconds: 0,
    setExerciseTimeSeconds: (exerciseTimeSeconds) => set({ exerciseTimeSeconds }),
}));