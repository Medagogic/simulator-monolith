// chatStore.ts
"use client"

import { create } from 'zustand';
import { CombatLogElement } from '@/src/scribe/scribetypes';


export function generateCombatLogElements(n: number): CombatLogElement[] {
  const types = [
    "Evt_CompletedIntervention",
    "Evt_StartTask",
    "Evt_Assessment",
    "Evt_TaskConsequence"
  ];
  const npcNames = ["Orc", "Goblin", "Dragon", "Troll"];
  const contents = [
    "Swing sword",
    "Cast spell",
    "Use potion",
    "Evade",
    "Parry"
  ];

  const combatLogElements: CombatLogElement[] = [];

  for (let i = 0; i < n; i++) {
    const randomType = types[Math.floor(Math.random() * types.length)];
    const randomNpcName = npcNames[Math.floor(Math.random() * npcNames.length)];
    const randomContent =
      contents[Math.floor(Math.random() * contents.length)];

    combatLogElements.push({
      timestamp: i,
      npc_name: randomNpcName,
      content: randomContent,
      type: randomType,
      extraField: "Some additional data"
    });
  }

  return combatLogElements;
}


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
