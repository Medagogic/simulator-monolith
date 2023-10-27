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



export const TEST_fullConnectionData: SIO_ConnectedDevices = {
  iv_access: [
      {
          location: 'left hand',
      },
      {
          location: 'right hand',
      }
  ],
  io_access: [
      {
          location: 'distal femur',
          side: 'left'
      },
      {
          location: 'distal femur',
          side: 'right'
      },
      {
          location: 'distal tibia',
          side: 'left'
      },
      {
          location: 'distal tibia',
          side: 'right'
      },
      {
          location: 'proximal tibia',
          side: 'left'
      },
      {
          location: 'proximal tibia',
          side: 'right'
      }
  ],
  ekg_connected: true,
  nibp: { },
  pulse_ox: {
      probe_position: "finger"
  },
};