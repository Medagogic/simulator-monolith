import { ScribeClient } from "@/src/scribe/ScribeClient";
import { DrClippyOutput } from "@/src/scribe/scribetypes";
import { useDrClippyStore } from "../storage/DrClippyStore";


export class DrClippyIO extends ScribeClient {
    on_dr_clippy_update(data: DrClippyOutput): void {
        console.log("DrClippyIO.on_dr_clippy_update", data);
        console.log(data);
        useDrClippyStore.getState().setDrClippyOutput(data);
    }
}