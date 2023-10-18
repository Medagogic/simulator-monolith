import { ScribeClient } from "@/src/scribe/ScribeClient";
import { VitalSigns } from "@/src/scribe/scribetypes";
import { usePatientStore } from "../sim-session/Patient/PatientStore";

export class PatientIO extends ScribeClient {
    on_patient_vitals_update(data: VitalSigns): void {
        console.log("on_patient_vitals_update", data);
        usePatientStore.getState().setVitals(data);
    }
}