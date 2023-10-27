// chatStore.ts
"use client"

import { create } from 'zustand';
import { APINPCData } from '@/src/api';


type TeamState = {
  teamById: { [key: string]: APINPCData };
  setNPCData(id: string, data: APINPCData): void;
  thinkingAbout: { [key: string]: string };
  setThinkingAbout(id: string, about: string | null): void;
};

export const useTeamStore = create<TeamState>((set, get) => {
  return {
    teamById: {},
    thinkingAbout: {},
    setNPCData: (id: string, data: APINPCData) => set(state => (
      {
        teamById: {
          ...state.teamById,
          [id]: data,
        }
      }
    )),
    setThinkingAbout: (id: string, about: string | null) => set(state => {
      const updatedThinkingAbout = { ...state.thinkingAbout };

      if (about === null) {
        delete updatedThinkingAbout[id];
      } else {
        updatedThinkingAbout[id] = about;
      }

      return {
        thinkingAbout: updatedThinkingAbout,
      };
    }
    ),
  };
});
