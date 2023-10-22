import React from 'react';

const NeonateInfo: React.FC = () => {
  return (
    <div className="bg-gray-700 text-white p-4 rounded-lg">
      <h1 className="text-2xl font-bold">Neonate - Hypoxic-Ischemic Encephalopathy (HIE)</h1>
      <div className="grid grid-cols-2 gap-4 mt-4">
        {[
          { label: "Age", value: "3 days" },
          { label: "Weight", value: "3.5 kg" },
          { label: "Allergies", value: "None" },
          { label: "ABCDE status", value: "Airway clear, Breathing irregular (periodic breathing), Circulation stable, Disability (clonic movements of one arm), Exposure (birth asphyxia noted)." },
          { label: "Medical Description", value: "Neonate presents with focal clonic seizures possibly secondary to hypoxic-ischemic injury during birth." },
          { label: "Condition/Cause", value: "Hypoxic-Ischemic Encephalopathy (HIE)" },
          { label: "Heart Rate", value: "165 bpm" },
          { label: "Respiratory Rate", value: "60 breaths/min" },
          { label: "Blood Pressure", value: "55/30 mmHg (normal range for neonates)" },
          { label: "Temperature", value: "36.5°C" },
          { label: "SpO2", value: "88% (critical; action required)" },
        ].map(({ label, value }, index) => (
          <div key={index} className="flex">
            <span className="font-semibold mr-2">{label}:</span>
            <span>{value}</span>
          </div>
        ))}
      </div>
      <div className="mt-4">
        <p className="text-sm">
          <span className="font-semibold">Simulation Instruction:</span> After initial IV/intranasal Midazolam, seizures stop but then return stronger. Phenobarbital administration leads to a significant drop in respiratory rate, challenging trainees in managing potential side effects.
        </p>
      </div>
    </div>
  );
};

export default NeonateInfo;
