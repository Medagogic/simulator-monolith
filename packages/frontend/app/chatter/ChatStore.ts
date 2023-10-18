// chatStore.ts
"use client"

import { create } from 'zustand';
import { io } from 'socket.io-client';
import { ChatterIO } from './ChatterIO';
import { useSocket } from '../socketio/SocketContext';
import { useEffect } from 'react';

export type ChatStoreMessage = {
  text: string;
  sender: string;
  date: Date;
};


type ChatState = {
  messages: ChatStoreMessage[];
  currentMessage: string;
  setCurrentMessage: (message: string) => void;
  isTyping: boolean;
  // initializeSocket: () => void;
  addMessage: (message: ChatStoreMessage) => void;
  setIsTyping: (status: boolean) => void;
  sendMessage: (message: string) => void;
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
    sendMessage: (messageText: string) => {
      console.log('sending message', messageText);

      const { addMessage } = get();

      const message: ChatStoreMessage = {
        text: messageText,
        sender: 'user',
        date: new Date(),
      };

      // Call the addMessage function to add the message to the state
      addMessage(message);
    }
  }
});
