import { ScribeClient } from "@/src/scribe/ScribeClient";
import { EvaluationChecklist, EvaluationChecklistItem } from "@/src/scribe/scribetypes";
import { useLearnerActionStore } from "../storage/LearneActionStore";


export class LearnerActionEvaluatorIO extends ScribeClient {
    on_learner_action_checklist(data: EvaluationChecklist): void {
        console.log("LearnerActionEvaluatorIO.on_learner_action_checklist", data);
        useLearnerActionStore.getState().setChecklist(data);
    }
}