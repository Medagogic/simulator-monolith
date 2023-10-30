import { EvaluationChecklist } from "@/src/scribe/scribetypes";
import { create } from "zustand";

type LearnerActionStore = {
    checklist: EvaluationChecklist | null;
    setChecklist: (checklist: EvaluationChecklist) => void;
};

export const useLearnerActionStore = create<LearnerActionStore>((set, get) => ({
  checklist: null,
  setChecklist: (checklist) => {
    set((state) => ({ checklist: checklist }));
  }

}));