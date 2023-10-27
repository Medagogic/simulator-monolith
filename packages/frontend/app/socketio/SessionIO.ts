import { ScribeClient } from "@/src/scribe/ScribeClient";
import { SIO_TimeUpdate } from "@/src/scribe/scribetypes";
import { useSessionStore } from "../storage/SessionStore";

export class SessionIO extends ScribeClient {
    on_time_update(data: SIO_TimeUpdate): void {
        useSessionStore.getState().setExerciseTimeSeconds(data.exercise_time_seconds);
    }
}