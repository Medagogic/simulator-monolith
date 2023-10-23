import React from 'react';

export interface ScenarioInfoProps {
  name: string;
  info: Record<string, string>;
  simulationInstruction: string;
}


const scenario1: ScenarioInfoProps = {
  name: "Neonate - Hypoxic-Ischemic Encephalopathy (HIE)",
  info: {
    "Age": "3 days",
    "Weight": "3.5 kg",
    "Allergies": "None",
    "ABCDE status": "Airway clear, Breathing irregular (periodic breathing), Circulation stable, Disability (clonic movements of one arm), Exposure (birth asphyxia noted)",
    "Medical Description": "Neonate presents with focal clonic seizures possibly secondary to hypoxic-ischemic injury during birth",
    "Condition/Cause": "Hypoxic-Ischemic Encephalopathy (HIE)",
    "Heart Rate": "165 bpm",
    "Respiratory Rate": "60 breaths/min",
    "Blood Pressure": "55/30 mmHg (normal range for neonates)",
    "Temperature": "36.5°C",
    "SpO2": "88% (critical; action required)"
  },
  simulationInstruction: "After initial IV/intranasal Midazolam, seizures stop but then return stronger. Phenobarbital administration leads to a significant drop in respiratory rate, challenging trainees in managing potential side effects"
};

const scenario2: ScenarioInfoProps = {
  name: "Infant - Febrile Seizure",
  info: {
    "Age": "8 months",
    "Weight": "7.5 kg",
    "Allergies": "None",
    "ABCDE status": "Airway clear, Breathing regular, Circulation stable, Disability (generalized tonic-clonic seizure), Exposure (fever of 39°C).",
    "Medical Description": "Infant presents with a typical febrile seizure in the setting of an upper respiratory tract infection.",
    "Condition/Cause": "Simple Febrile Seizure",
    "Heart Rate": "155 bpm",
    "Respiratory Rate": "34 breaths/min",
    "Blood Pressure": "75/45 mmHg",
    "Temperature": "39.4°C",
    "SpO2": "95%"
  },
  simulationInstruction: "Diazepam administration fails to stop the seizures. Phenobarbital stops the seizures, but then trainees should monitor for potential side effects, excluding hypoglycemia which isn't a direct side effect."
};

const scenario3: ScenarioInfoProps = {
  name: "Toddler - Dravet Syndrome",
  info: {
    "Age": "2 years",
    "Weight": "12 kg",
    "Allergies": "Allergic to phenobarbital",
    "ABCDE status": "Airway clear, Breathing regular, Circulation stable, Disability (myoclonic jerks followed by prolonged tonic-clonic seizure), Exposure (history of developmental delay and frequent prolonged seizures).",
    "Medical Description": "Child with known Dravet syndrome presents with a prolonged seizure episode likely triggered by fever.",
    "Condition/Cause": "Dravet Syndrome",
    "Heart Rate": "140 bpm",
    "Respiratory Rate": "36 breaths/min",
    "Blood Pressure": "90/50 mmHg",
    "Temperature": "38.9°C",
    "SpO2": "92%"
  },
  simulationInstruction: "Seizure activity halts after the first dose of IV Midazolam but returns more intensely. Trainees should then consider second-line antiseizure medication, avoiding phenobarbital due to the known allergy."
};

const scenario4: ScenarioInfoProps = {
  name: "School-Aged Child - Previous Brain Injury",
  info: {
    "Age": "8 years",
    "Weight": "25 kg",
    "Allergies": "None",
    "ABCDE status": "Airway clear, Breathing regular, Circulation stable, Disability (focal seizure with secondary generalization), Exposure (scar on the scalp from a previous trauma)",
    "Medical Description": "The child, with a history of traumatic brain injury a year ago, now presents with new-onset seizures.",
    "Condition/Cause": "Post-Traumatic Epilepsy (PTE)",
    "Heart Rate": "110 bpm",
    "Respiratory Rate": "28 breaths/min",
    "Blood Pressure": "100/60 mmHg",
    "Temperature": "37.1°C",
    "SpO2": "97%"
  },
  simulationInstruction: "The child doesn't respond to the first dose of IV Midazolam, prompting another dose. After Fosphenytoin administration, simulate an allergic reaction, challenging trainees to manage this while also addressing the seizures."
};

const scenario5: ScenarioInfoProps = {
  name: "Early-Teen - Unknown Seizure Etiology",
  info: {
    "Age": "13 years",
    "Weight": "50 kg",
    "Allergies": "Allergic to phenytoin",
    "ABCDE status": "Airway clear, Breathing regular, Circulation stable, Disability (absence seizure with intermittent myoclonic jerks), Exposure (no obvious triggers).",
    "Medical Description": "The teenager presents with an absence seizure that later progressed to involve myoclonic jerks, with no identifiable etiology on initial assessment.",
    "Condition/Cause": "Juvenile Myoclonic Epilepsy (JME)",
    "Heart Rate": "105 bpm",
    "Respiratory Rate": "20 breaths/min",
    "Blood Pressure": "110/70 mmHg",
    "Temperature": "37.3°C",
    "SpO2": "96%"
  },
  simulationInstruction: "Seizure activity diminishes after IV Midazolam but doesn't stop. Second-line treatment with an antiseizure medication other than phenytoin or Fosphenytoin should be considered due to the known allergy. After administration, simulate brief respiratory depression, testing trainees' skills in managing this complication."
};


export const scenarios: ScenarioInfoProps[] = [
  scenario1,
  scenario2,
  scenario3,
  scenario4,
  scenario5
]


const ScenarioInfo: React.FC<ScenarioInfoProps> = (scenario: ScenarioInfoProps) => {
  return (
    <div className="bg-gray-700 text-white p-4 rounded-lg">
      <h1 className="text-2xl font-bold">{scenario.name}</h1>
      <div className="grid grid-cols-1 gap-4 mt-4">
        {Object.entries(scenario.info).map(([label, value], index) => (
          <div key={index} className="flex">
            <span className="font-semibold mr-2 w-36">{label}:</span>
            <span>{value}</span>
          </div>
        ))}
      </div>
      <div className="mt-4">
        <p className="text-sm">
          <span className="font-semibold">Simulation Instruction:</span> {scenario.simulationInstruction}
        </p>
      </div>
    </div>
  );
};

export default ScenarioInfo;
