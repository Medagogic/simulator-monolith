// chatStore.ts
"use client"

import { create } from 'zustand';
import { CombatLogElement } from '@/src/scribe/scribetypes';


type CombatLogState = {
  logs: CombatLogElement[];
  setLogs: (data: CombatLogElement[]) => void;
};

export const useCombatLogStore = create<CombatLogState>((set, get) => {
  return {
    logs: [],
    setLogs: (data: CombatLogElement[]) => set({ logs: data }),
  };
});
