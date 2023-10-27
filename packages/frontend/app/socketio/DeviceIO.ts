import { ScribeClient } from "@/src/scribe/ScribeClient";
import { SIO_ConnectedDevices, VitalSigns } from "@/src/scribe/scribetypes";
import { useDeviceStore } from "../storage/DeviceStore";

export class DeviceIO extends ScribeClient {
    on_device_update(data: SIO_ConnectedDevices): void {
        useDeviceStore.getState().setDeviceState(data);
    }
}