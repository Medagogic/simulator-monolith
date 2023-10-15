// chatStore.ts
"use client"

import { create } from 'zustand';
import { io } from 'socket.io-client';


export type Message = {
  text: string;
  sender: 'user' | 'system' | 'assistant';
  date: Date;
};


type ChatState = {
  messages: Message[];
  currentMessage: string;
  setCurrentMessage: (message: string) => void;
  isTyping: boolean;
  initializeSocket: (namespace: string) => void;
  addMessage: (message: Message) => void;
  setIsTyping: (status: boolean) => void;
  sendMessage: (message: string) => void;
  socket?: any;
  attachments: any[];
};

export const useChatStore = create<ChatState>((set, get) => {
  return {
    messages: [],
    currentMessage: '',
    isTyping: false,
    attachments: [],
    initializeSocket: (namespace) => {
      const socket = io(`ws://127.0.0.1/${namespace}`);

      socket.on('receiveMessage', (message) => {
        set((state) => ({ messages: [...state.messages, message] }));
      });

      socket
        .on("connect", () => {
          console.log("SOCKET CONNECTED!", socket.id);
          // Update the socket in the global state when connected
          set({ socket });
        })
        .on("disconnect", () => {
          console.log("SOCKET DISCONNECTED!");
          // Set socket to null in the global state when disconnected
          set({ socket: null });
        });

      set({ socket });
    },
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
    
      const { socket, addMessage } = get();
    
      const message: Message = {
        text: messageText,
        sender: 'user',
        date: new Date(),
      };
    
      // Call the addMessage function to add the message to the state
      addMessage(message);
    
      if (socket) {
        socket.emit('newMessage', messageText);
      }
    }
  }
});