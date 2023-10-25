import { ScribeClient } from "@/src/scribe/ScribeClient";
import { VitalSigns } from "@/src/scribe/scribetypes";
import { usePatientStore } from "../storage/PatientStore";

export class PatientIO extends ScribeClient {
    on_patient_vitals_update(data: VitalSigns): void {
        usePatientStore.getState().setVitals(data);
    }
}