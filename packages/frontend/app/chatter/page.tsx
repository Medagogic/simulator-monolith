"use client"

import React, { useEffect } from 'react';
import ChatterBox from './ChatterBox';
import "./page.css"
import { SocketProvider } from '../socketio/SocketContext';


const ChatterboxTestPage: React.FC = () => {
  return (
    <div style={{ width: "100%", height: "100%" }} className='flex flex-col base'>
      <SocketProvider session_id='default-session'>
        <ChatterBox/>
      </SocketProvider>
    </div>
  );
}

export default ChatterboxTestPage;
