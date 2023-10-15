// components/ObjectivesList.tsx
import React from 'react';

export interface Objective {
  description: string;
  completed: boolean; // true for pass (green check mark), false for fail (red cross)
}

interface ObjectivesListProps {
  objectives: Objective[];
}

export const ObjectivesList: React.FC<ObjectivesListProps> = ({ objectives }) => {
    return (
      <div className="flex flex-col space-y-2 p-3 max-h-96 overflow-auto bg-gray-700 text-white">
        <h2>
            Exercise Progress
        </h2>
        {objectives.map((objective, index) => {
          const iconClass = objective.completed ? 'text-green-500' : 'text-red-500';
          const icon = objective.completed ? '✔️' : '❌';
  
          return (
            <div key={index} className="flex items-center space-x-2 text-xs">
              <div className={iconClass}>
                <span>{icon}</span>
              </div>
              <div className="flex-grow">
                <span>{objective.description}</span>
              </div>
            </div>
          );
        })}
      </div>
    );
  };
