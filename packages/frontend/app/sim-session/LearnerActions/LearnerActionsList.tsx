// components/ObjectivesList.tsx
import { useLearnerActionStore } from '@/app/storage/LearneActionStore';
import React from 'react';


export const LearnerActionsList: React.FC = () => {
  const actionChecklist = useLearnerActionStore((state) => state.checklist);

  function hasData() {
    return actionChecklist && actionChecklist.items != null;
  }

  function hasAnyCompleted() {
    return hasData() && actionChecklist!.items!.some((learnerAction: any) => learnerAction.completed);
  }

  const renderActionItem = (learnerAction: any, index: number) => {
    return (
      <div key={index} className="flex items-center space-x-2 text-xs">
        <div className="text-green-500">
          <span>✔️</span>
        </div>
        <div className="flex-grow text-xs">
          <span>{learnerAction.text}</span>
        </div>
      </div>
    );
  };

  const renderContent = () => {
    if (!hasData()) {
      return <span className='text-xs text-slate-400'>Loading...</span>;
    }
    if (!hasAnyCompleted()) {
      return <span className='text-xs text-slate-400'>No progress yet</span>;
    }

    return actionChecklist!.items!
      .filter((learnerAction: any) => learnerAction.completed)
      .map(renderActionItem);
  };

  return (
    <div className="flex flex-col space-y-2 p-3 max-h-96 overflow-auto bg-gray-700 text-white">
      <h2>Exercise Progress</h2>
      {renderContent()}
    </div>
  );
};