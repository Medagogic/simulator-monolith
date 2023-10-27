"use client"
import React, { useState, useEffect, FC, FormEvent } from 'react';
import { io, Socket } from "socket.io-client";
import Link from 'next/link';
import { SocketProvider } from './socketio/SocketContext';
import SimSessionPage from './sim-session/page';
import { useSessionStore } from './storage/SessionStore';

const Index: FC = () => {
  const sessionName: string | undefined = useSessionStore((state) => state.sessionName);
 
  return (
    <main style={{"height": "100vh", width:"100vw"}}>
      {sessionName !== undefined && (
      <SocketProvider session_id='default-session'>
        <SimSessionPage sessionName={sessionName}/>
      </SocketProvider>
      )}
      {sessionName === undefined && (
        <div className="flex flex-col items-center justify-center h-full">
          <h1 className="text-4xl font-bold">Medagogic Simulator</h1>
          <div className="flex flex-col items-center justify-center gap-2">
            <h1>No session id</h1>
          </div>
        </div>
      )}
    </main>
  );
};

export default Index;
