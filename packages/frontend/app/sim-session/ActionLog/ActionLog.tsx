// components/ActionLog.tsx
import React from 'react';

export enum ActionType {
  Intervention = 'intervention',
  Preparation = 'preparation',
  Assessment = 'assessment',
  Communication = 'communication',
}

export interface ActionLogEntry {
  timestamp: Date;
  staffName: string; // changed from 'character' to 'staffName' for clarity in a medical context
  action: string;
  actionType: ActionType;
}

interface ActionLogProps {
  logs: ActionLogEntry[];
}

const actionTypeColors: Record<ActionType, string> = {
  [ActionType.Intervention]: 'text-amber-600', // Amber, being a warm color, draws attention without the urgency of red.
  [ActionType.Preparation]: 'text-blue-600', // Blue is calm and stable, ideal for preparation stages.
  [ActionType.Assessment]: 'text-cyan-600', // Cyan, as a mix of blue and green, suggests careful consideration, suitable for assessments.
  [ActionType.Communication]: 'text-purple-600', // Purple can signify communication, being a mix of calm blue and energetic red.
  // ... any other action types and their colors
};

const getActionColor = (actionType: ActionType): string => {
  // Return the corresponding color or fall back to a default color if the action type is not found
  return actionTypeColors[actionType] || 'text-gray-500'; // Neutral gray as the default color
};

export const ActionLog: React.FC<ActionLogProps> = ({ logs }) => {
  return (
    <div className="flex flex-col space-y-2 p-3 max-h-96 overflow-auto border border-gray-300 bg-gray-700 text-white">
      {logs.map((log, index) => (
        <div key={index} className="flex w-full items-center space-x-2 text-xs"> {/* Added 'text-xs' here for font sizing */}
          <div className="flex-shrink-0">
            <span>[{log.timestamp.toLocaleTimeString()}]</span>
          </div>
          <div className={`flex-grow flex items-center ${getActionColor(log.actionType)}`}>
            <span className="font-bold mr-2">{log.staffName}</span>
            <span>{log.action}</span>
          </div>
        </div>
      ))}
    </div>
  );
};