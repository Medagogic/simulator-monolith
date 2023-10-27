// chatStore.ts
"use client"

import { create } from 'zustand';
import { SIO_ConnectedDevices } from '@/src/scribe/scribetypes';


type ConnectedDeviceState = {
  connectedDevices: SIO_ConnectedDevices;
  setDeviceState(data: SIO_ConnectedDevices): void;
};

export const useDeviceStore = create<ConnectedDeviceState>((set, get) => {
  return {
    connectedDevices: {} as SIO_ConnectedDevices,
    setDeviceState: (data) => set({ connectedDevices: data })
  };
});
