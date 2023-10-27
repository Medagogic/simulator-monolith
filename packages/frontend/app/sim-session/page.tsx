"use client"

import React from 'react';
import { StaffDefinition } from './StaffCard';
import VitalSignsDisplay from './VitalSignsDisplay';
import { ExerciseCreationABCDE, ExerciseCreationVitalSigns } from '@/src/api';
import { VitalSigns } from '@/src/scribe/scribetypes';
import ChatterBox from '../chatter/page';
import "./page.css"
import Clippy from './Clippy/Clippy';
import ABCDEList from './ABCDEList/ABCDEList';
import StaffList from './StaffList/StaffList';
import PatientVisualization from './Patient/PatientVisualization';
import { ActionLog } from './ActionLog/ActionLog';
import TimeDisplay from './TimeDisplay/TimeDisplay';
import { Objective, ObjectivesList } from './ObjectivesList/ObjectivesList';
import { SocketProvider } from '../socketio/SocketContext';
import PatientMonitor from './Monitor/PatientMonitor';
import { APIProvider } from '../socketio/APIContext';
import { useSessionStore } from '../storage/SessionStore';



const staffData: StaffDefinition[] = [
  { name: 'Dr. Smith', role: 'Doctor', activity: 'Checking vitals' },
  { name: 'Jane Doe', role: 'Nurse', activity: 'Administering medication' },
  { name: 'John Doe', role: 'Anaesthetist', activity: 'Monitoring anesthesia' },
  { name: 'Dr. Pooper', role: 'Doctor', activity: 'Checking vitals' },
  { name: 'Jane Doe', role: 'Nurse' },
];

const vitalSignsForABCDEList: ExerciseCreationVitalSigns = {
  temperature: '38.6 °C',
  heartRate: '75 bpm',
  respiratoryRate: '16 bpm',
  bloodPressure: '120/80 mmHg',
  bloodGlucose: '90 mg/dL',
  oxygenSaturation: '98%',
  capillaryRefill: '<2 seconds'
};

const vitalSignsForDisplay: VitalSigns = {
  temperature: 38.6,
  heart_rate: 75,
  respiratory_rate: 16,
  blood_pressure: { systolic: 120, diastolic: 80 },
  blood_glucose: 90,
  oxygen_saturation: 98,
  capillary_refill: 2
};

const abcdeData: ExerciseCreationABCDE = {
  a: 'Airway patent.',
  b: 'Laboured breathing, right chest pain.',
  c: 'Tachycardic.',
  d: 'AVPU: A',
  e: 'No external bleeding or rashes.',
};

const objectives: Objective[] = [
  { description: 'Assess airway as priority.', completed: true },
  { description: 'Resolve airway obstruction.', completed: false },
  { description: 'Administer 50mg medication A.', completed: true },
  // ... other objectives
];

export interface SimSessionPageProps {
  sessionName: string;
}


const SimSessionPage: React.FC<SimSessionPageProps> = ({ sessionName }) => {


  function handleClippySuggestion(data: { description: string, command: string }) {
    console.log(data.command);
  }

  return (
    <SocketProvider session_id={sessionName}>
      <APIProvider sessionId={sessionName}>
        <div className='page-container'>
          <div className='toolbar'>
            <div style={{ flex: 1 }}>
              Medagogic Simulator - {sessionName}
            </div>

            <div style={{ display: 'flex', justifyContent: 'center', position: 'absolute', left: 0, right: 0 }}>
              <TimeDisplay />
            </div>

            <div style={{ flex: 1, display: 'flex', justifyContent: 'flex-end' }}>
              <h1 className="text-white">

              </h1>
            </div>
          </div>

          <div className="main-page gap-2">
            <div className='column' style={{ flex: "1 0 auto" }}>
              {/* <VitalSignsDisplay debugVitalSigns={vitalSignsForDisplay} /> */}
              <PatientVisualization />
              {/* <ABCDEList abcdeData={abcdeData} vitalSigns={vitalSignsForABCDEList} /> */}
              <PatientMonitor />

            </div>

            <div className='column gap-2' style={{ flex: "1 0 auto", width: "50%" }}>
              <div className="flex-shrink h-1/4">
                <ActionLog />
              </div>
              <div className="flex-auto flex flex-grow overflow-hidden h-full">
                <div className="flex-auto">
                  <ChatterBox />
                </div>
                <div className="flex-shrink">
                  <StaffList />
                </div>
              </div>

            </div>
            <div className='column' style={{ flex: "0 1 auto" }}>
              <ObjectivesList objectives={objectives} />
              <div className="self-end w-full">
                <Clippy onClick={(data) => { handleClippySuggestion(data) }} />
              </div>
            </div>

          </div>
        </div>
      </APIProvider>
    </SocketProvider>

  );
}

export default SimSessionPage;
