import { VitalSigns } from "@/src/scribe/scribetypes";
import { create } from "zustand";

type PatientStore = {
    vitals: VitalSigns | null;
    setVitals: (vitals: VitalSigns) => void;
};

export const usePatientStore = create<PatientStore>((set, get) => ({
    vitals: null,

    setVitals: (vitals) => set({ vitals }),
}));