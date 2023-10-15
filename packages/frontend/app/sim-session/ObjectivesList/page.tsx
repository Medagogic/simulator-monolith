import React from 'react';
import { ObjectivesList, Objective } from './ObjectivesList'; // Adjust the import statement as needed

const ObjectivesListTest: React.FC = () => {
  // Sample objectives data
  const objectives: Objective[] = [
    { description: 'Complete the patient’s health assessment.', completed: true },
    { description: 'Update the medication list.', completed: false },
    // ... other objectives
  ];

  return <ObjectivesList objectives={objectives} />;
};

export default ObjectivesListTest;
