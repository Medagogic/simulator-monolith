"use client"
import React, { useState, useEffect, FC, FormEvent } from 'react';
import { io, Socket } from "socket.io-client";
import Link from 'next/link';
import { SocketProvider } from './socketio/SocketContext';
import SimSessionPage from './sim-session/page';

const Index: FC = () => {
 
  return (
    <main style={{"height": "100vh"}}>
      <SocketProvider session_id='default-session'>
        <SimSessionPage />
      </SocketProvider>
    </main>
  );
};

export default Index;
