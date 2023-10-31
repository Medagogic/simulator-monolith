"use client"
import React, { useState, useEffect, FC, FormEvent } from 'react';
import { io, Socket } from "socket.io-client";
import Link from 'next/link';
import { SocketProvider, useSessionIO } from './socketio/SocketContext';
import SimSessionPage from './sim-session/page';
import { useSessionStore } from './storage/SessionStore';
import { APIProvider } from './socketio/APIContext';
import { FaSpinner } from "react-icons/fa";
import "./page.css"


const ConnectedSwitcher: FC = () => {
  const [isFading, setIsFading] = useState(true);
  const connected = useSessionIO()?.socket.connected;


  useEffect(() => {
    if (connected) {
      setIsFading(false);
    }
  }, [connected]);

  return (
    <>
      <div className={`connecting-page ${isFading ? '' : 'fade-out pointer-events-none'}`}>
        <WaitingToConnectPage />
      </div>
      {connected && <SimSessionPage />}
    </>
  );
}


const WaitingToConnectPage: FC = () => {
  const sessionName: string | undefined = useSessionStore((state) => state.sessionName);

  const containerStyle = {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: '100vh',
    width: '100vw',
    backgroundColor: '#222',
    color: "#bbb"
  };

  const spinnerStyle = {
    animation: 'spin 1s linear infinite',
    marginRight: '10px',
  };
  

  return (
    <div style={containerStyle}>
      <FaSpinner style={spinnerStyle} />
      Connecting to {sessionName}
    </div>
  );
};

const Index: FC = () => {
  const sessionName: string | undefined = useSessionStore((state) => state.sessionName);

  return (
    <main style={{ "height": "100vh", width: "100vw" }}>
      {sessionName !== undefined && (
        <SocketProvider session_id={sessionName}>
          <APIProvider sessionId={sessionName}>
            <ConnectedSwitcher />
          </APIProvider>
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
