// chatStore.ts
"use client"

import { create } from 'zustand';
import { ChatterIO } from './ChatterIO';
import { MessageFromNPC, ChatEvent, HumanMessage } from "@/src/scribe/scribetypes";

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
};

export const useChatStore = create<ChatState>((set, get) => {
  return {
    messages: [],
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
  }
});
