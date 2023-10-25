// chatStore.ts
"use client"

import { create } from 'zustand';
import { APINPCData } from '@/src/api';


type TeamState = {
  teamById: {[key: string]: APINPCData};
  setNPCData(id: string, data: APINPCData): void;
};

export const useTeamStore = create<TeamState>((set, get) => {
  return {
    teamById: {},
    setNPCData: (id: string, data: APINPCData) => set(state => (
      {
        teamById: {
          ...state.teamById,
          [id]: data,
        }
      }
    )),
  };
});
