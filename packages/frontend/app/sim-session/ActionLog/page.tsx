import React from 'react';
import { ActionLog, ActionLogEntry, ActionType } from './ActionLog'; // Adjust the path if necessary

const combatLogs: ActionLogEntry[] = [
  { timestamp: new Date(), staffName: 'Aragon', action: 'assess capillary refill time', actionType: ActionType.Assessment },
  { timestamp: new Date(), staffName: 'Gandalf', action: 'obtained IV access', actionType: ActionType.Intervention },
  { timestamp: new Date(), staffName: 'Merry', action: 'called for xray prep', actionType: ActionType.Communication },
  { timestamp: new Date(), staffName: 'Pippin', action: 'prepared 1L of saline', actionType: ActionType.Preparation },
  // more log entries...
];

const ActionLogTestPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-100 py-6 flex justify-center sm:py-12">
      {/* Container div modified to take up a third of the page's width */}
      <div className="w-1/3 py-3"> 
        {/* other components or HTML elements */}
        <ActionLog logs={combatLogs} />
      </div>
    </div>
  );
};

export default ActionLogTestPage;
