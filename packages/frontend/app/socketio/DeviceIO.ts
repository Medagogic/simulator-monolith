import { ScribeClient } from "@/src/scribe/ScribeClient";
import { SIO_ConnectedDevices } from "@/src/scribe/scribetypes";
import { useDeviceStore } from "../storage/DeviceStore";

export class DeviceIO extends ScribeClient {
    on_device_update(data: SIO_ConnectedDevices): void {
        // console.log("DeviceIO.on_device_update", data);
        useDeviceStore.getState().setDeviceState(data);
    }
}