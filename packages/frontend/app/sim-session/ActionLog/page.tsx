import React from 'react';
import { ActionLog } from './ActionLog'; // Adjust the path if necessary

const ActionLogTestPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-100 py-6 flex justify-center sm:py-12">
      {/* Container div modified to take up a third of the page's width */}
      <div className="w-1/3 py-3"> 
        {/* other components or HTML elements */}
        <ActionLog />
      </div>
    </div>
  );
};

export default ActionLogTestPage;
