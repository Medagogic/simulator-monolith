import { ScribeClient } from "@/src/scribe/ScribeClient";
import { ExposedVitalSigns } from "@/src/scribe/scribetypes";
import { usePatientStore } from "../storage/PatientStore";

export class PatientIO extends ScribeClient {
    on_patient_vitals_update(data: ExposedVitalSigns): void {
        usePatientStore.getState().setVitals(data);
    }
}
