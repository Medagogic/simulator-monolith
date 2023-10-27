"use client"

// components/ActionLog.tsx
import { generateCombatLogElements, useCombatLogStore } from '@/app/storage/CombatLogStore';
import React, { use, useEffect, useRef } from 'react';


interface ActionLogProps {

}

const actionTypeColors: Record<string, string> = {
  ["Evt_CompletedIntervention"]: 'text-amber-600',
  ["Evt_StartTask"]: 'text-blue-600',
  ["Evt_Assessment"]: 'text-cyan-600',
  ["Evt_TaskConsequence"]: 'text-purple-600',
};

const getActionColor = (actionType: string): string => {
  return actionTypeColors[actionType] || 'text-gray-500'; // Neutral gray as the default color
};

export const ActionLog: React.FC<ActionLogProps> = ({  }) => {
  const logs = useCombatLogStore((state) => state.logs);
  const setLogs = useCombatLogStore((state) => state.setLogs);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }
  }, [logs]);

  useEffect(() => {
    setLogs(generateCombatLogElements(100));
  }, []);

  return (
    <div ref={containerRef} className="flex flex-col space-y-2 p-3 max-h-96 overflow-auto border border-gray-300 bg-gray-700 text-white h-full">
      {logs.map((log, index) => (
        <div key={index} className="flex w-full items-center space-x-2 text-xs"> {/* Added 'text-xs' here for font sizing */}
          <div className="flex-shrink-0">
            <span>[{log.timestamp}]</span>
          </div>
          <div className={`flex-grow flex items-center ${getActionColor(log.type)}`}>
            <span className="font-bold mr-2">{log.npc_name}</span>
            <span>{log.content}</span>
          </div>
        </div>
      ))}
    </div>
  );
};