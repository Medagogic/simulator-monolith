// SomeComponentOrPage.tsx
"use client"

import React, { useState } from 'react';
import BriefingModal from './BriefingModal';

const SomeComponentOrPage: React.FC = () => {
  const [isModalOpen, setModalOpen] = useState(false);

  return (
    <div>
      <button
        className="bg-blue-500 text-white p-2 rounded hover:bg-blue-700"
        onClick={() => setModalOpen(true)}
      >
        Show Briefing
      </button>

      <BriefingModal
        title="Scenario Introduction"
        content="Welcome to the medical training simulation. This scenario will test your skills in..."
        isOpen={isModalOpen}
        onClose={() => setModalOpen(false)}
      />
    </div>
  );
};

export default SomeComponentOrPage;