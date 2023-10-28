// chatStore.ts
"use client"

import { create } from 'zustand';
import { ChatterIO } from '../socketio/ChatterIO';
import { MessageFromNPC, ChatEvent, HumanMessage } from "@/src/scribe/scribetypes";
import { getDummyMessages } from './_DummyChatData';

export type ChatStoreMessage = {
  message: MessageFromNPC | HumanMessage | ChatEvent;
  type: "npc" | "human" | "event";
};


type ChatState = {
  messages: ChatStoreMessage[];
  currentMessage: string;
  setCurrentMessage: (message: string) => void;
  isTyping: boolean;
  addMessage: (message: ChatStoreMessage) => void;
  setIsTyping: (status: boolean) => void;
  attachments: any[];
  chatterio?: ChatterIO;
  toNPCId?: string;
  setToNPCId: (npcId?: string) => void;
};

export const useChatStore = create<ChatState>((set, get) => {
  return {
    messages: [], //getDummyMessages() as unknown as ChatStoreMessage[],
    currentMessage: '',
    isTyping: false,
    attachments: [],
    setCurrentMessage: (message) => {
      set({ currentMessage: message });
    },
    addMessage: (message) => {
      set((state) => ({ messages: [...state.messages, message] }));
    },
    setIsTyping: (status) => {
      set({ isTyping: status });
    },
    setToNPCId: (npcId) => {
      set({ toNPCId: npcId });
    },
  }
});
