
import { create } from "zustand";

type SessionStore = {
    sessionName: string | undefined;
    setSessionName: (sessionName: string) => void;
    exerciseTimeSeconds: number;
    setExerciseTimeSeconds: (exerciseTimeSeconds: number) => void;
};

export const useSessionStore = create<SessionStore>((set, get) => ({
    sessionName: "default-session",
    setSessionName: (sessionName) => set({ sessionName }),
    exerciseTimeSeconds: 0,
    setExerciseTimeSeconds: (exerciseTimeSeconds) => set({ exerciseTimeSeconds }),
}));