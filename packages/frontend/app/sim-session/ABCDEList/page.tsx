import { ExerciseCreationABCDE, ExerciseCreationVitalSigns } from "@/src/api";
import ABCDEList from "./ABCDEList";


const vitalSignsData: ExerciseCreationVitalSigns = {
  temperature: '38.6 °C',
  heartRate: '75 bpm',
  respiratoryRate: '16 bpm',
  bloodPressure: '120/80 mmHg',
  bloodGlucose: '90 mg/dL',
  oxygenSaturation: '98%',
  capillaryRefill: '<2 seconds',
};

const abcdeData: ExerciseCreationABCDE = {
  a: 'Description for A',
  b: 'Description for B',
  c: 'Description for C',
  d: 'Description for D',
  e: 'Description for E',
};

const ABCDEListTest = () => {
  return (
    <div style={{
        width: "25rem"
    }}>
      <ABCDEList abcdeData={abcdeData} vitalSigns={vitalSignsData} />
    </div>
  );
};

export default ABCDEListTest;