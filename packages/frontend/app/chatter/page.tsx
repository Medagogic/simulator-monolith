"use client"

import React, { useEffect } from 'react';
import ChatterBox from './ChatterBox';
import "./page.css"
import { useChatStore } from './ChatStore';


const ChatterboxTestPage: React.FC = () => {
  const namespace = "desired_namespace"; 
  const initializeSocket = useChatStore((state) => state.initializeSocket);

  useEffect(() => {
    initializeSocket(namespace);
  }, [namespace, initializeSocket]);
  
  return (
    <div style={{ width: "100%", height: "100%" }} className='flex flex-col base'>
      <ChatterBox/>
    </div>
  );
}

export default ChatterboxTestPage;
