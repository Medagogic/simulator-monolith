import { DrClippyOutput } from "@/src/scribe/scribetypes";
import { create } from "zustand";

type PatientStore = {
    drClippyOutput: DrClippyOutput | null;
    setDrClippyOutput: (drClippyOutput: DrClippyOutput) => void;
};

export const useDrClippyStore = create<PatientStore>((set, get) => ({
    drClippyOutput: {} as DrClippyOutput,

    setDrClippyOutput: (drClippyOutput) => {
        set((state) => 
            ({ drClippyOutput: drClippyOutput })
        );
    },
}));