"use client"

import React, { useState } from 'react';
import ScenarioInfo, { ScenarioInfoProps, scenarios } from './ScenarioInfo';
import { FiArrowRight } from 'react-icons/fi';

const ScenarioReviewPage: React.FC = () => {
  const [selectedScenario, setSelectedScenario] = useState<ScenarioInfoProps | null>(null);

  const handleScenarioClick = (scenario: ScenarioInfoProps) => {
    setSelectedScenario(scenario);
  };

  const handleSelectButtonClick = () => {
    // Add your logic here for when the select button is clicked
  };

  return (
    <div className="h-screen w-screen flex bg-gray-700 text-white relative">
      <div className="w-1/4 h-full overflow-y-auto bg-gray-600 p-4">
        <div className='text-lg font-semibold'>
          Generated Scenarios
        </div>
        <ul>
          {scenarios.map((scenario, index) => (
            <li 
              key={index} 
              className={`text-sm cursor-pointer p-2 m-2 rounded ${selectedScenario && selectedScenario.name === scenario.name ? 'bg-gray-500' : 'hover:bg-gray-500'}`}
              onClick={() => handleScenarioClick(scenario)}
            >
              {scenario.name}
            </li>
          ))}
        </ul>
      </div>
      <div className="w-3/4 h-full flex justify-center">
      {selectedScenario ? (
          <ScenarioInfo
            name={selectedScenario.name}
            info={selectedScenario.info}
            simulationInstruction={selectedScenario.simulationInstruction}
          />
        ) : (
          <div>Select a scenario</div>
        )}
      </div>
      <button 
        onClick={handleSelectButtonClick}
        className="absolute bottom-4 right-4 w-16 h-16 bg-blue-500 rounded-full flex items-center justify-center text-white text-2xl shadow-lg hover:bg-blue-600 focus:outline-none focus:border-blue-700 focus:ring focus:ring-blue-200"
      >
        <FiArrowRight size={24} />
      </button>
    </div>
  );
};

export default ScenarioReviewPage;
