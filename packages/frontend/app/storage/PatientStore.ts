import { ExposedVitalSigns } from "@/src/scribe/scribetypes";
import { create } from "zustand";

type PatientStore = {
    vitals: ExposedVitalSigns | null;
    setVitals: (vitals: ExposedVitalSigns) => void;
};

export const usePatientStore = create<PatientStore>((set, get) => ({
    vitals: null,

    setVitals: (vitals) => {
        set((state) => 
            ({ vitals: vitals })
        );
    },
}));