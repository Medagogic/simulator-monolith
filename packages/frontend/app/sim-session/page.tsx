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
import StaffList, { StaffMemberData } from './StaffList/StaffList';
import PatientVisualization from './Patient/PatientVisualization';
import { ActionLog, ActionLogEntry } from './ActionLog/ActionLog';
import TimeDisplay from './TimeDisplay/TimeDisplay';
import { Objective, ObjectivesList } from './ObjectivesList/ObjectivesList';
import { SocketProvider } from '../socketio/SocketContext';
import PatientMonitor from './Monitor/PatientMonitor';
import { APIProvider } from '../socketio/APIContext';



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

const actionLogs: ActionLogEntry[] = [
  // { timestamp: new Date(), staffName: 'Aragon', action: 'assess capillary refill time', actionType: ActionType.Assessment },
  // { timestamp: new Date(), staffName: 'Gandalf', action: 'obtained IV access', actionType: ActionType.Intervention },
  // { timestamp: new Date(), staffName: 'Merry', action: 'called for xray prep', actionType: ActionType.Communication },
  // { timestamp: new Date(), staffName: 'Pippin', action: 'prepared 1L of saline', actionType: ActionType.Preparation },
];

const objectives: Objective[] = [
  { description: 'Assess airway as priority.', completed: true },
  { description: 'Resolve airway obstruction.', completed: false },
  { description: 'Administer 50mg medication A.', completed: true },
  // ... other objectives
];

const SimSessionPage: React.FC = () => {
  function handleClippySuggestion(data: { description: string, command: string }) {
    console.log(data.command);
  }

  function getStaffData(): StaffMemberData[] {
    return staffData.map((staff, index) => {
      return {
        id: index.toString(),
        name: staff.name,
        specialty: staff.role,
        activity: staff.activity
      }
    });
  }

  return (
    <SocketProvider session_id='default-session'>
      <APIProvider sessionId="default-session">
      <div style={{ width: "100%", height: "100%" }} className='flex flex-col base'>
        <div className='toolbar' style={{ maxWidth: "100%", display: 'flex', flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' }}>
          <div style={{ flex: 1 }}>
            Medagogic Simulator
          </div>

          <div style={{ display: 'flex', justifyContent: 'center', position: 'absolute', left: 0, right: 0 }}>
            <TimeDisplay />
          </div>

          <div style={{ flex: 1, display: 'flex', justifyContent: 'flex-end' }}>
            <h1 className="text-white">

            </h1>
          </div>
        </div>

        <div style={{ "width": "100%", "height": "100%" }} className='flex flex-row'>
          <div className='flex flex-col flex-auto gap-2 m-2' style={{ width: "100%", height: "100%" }}>
            {/* <VitalSignsDisplay debugVitalSigns={vitalSignsForDisplay} /> */}
            <PatientVisualization />
            {/* <ABCDEList abcdeData={abcdeData} vitalSigns={vitalSignsForABCDEList} /> */}
            <PatientMonitor />

          </div>
          
          <div className='flex-auto m-2 flex flex-col gap-2' style={{ "width": "100%" }}>
            <div>
              <ActionLog logs={actionLogs} />
            </div>
            <div className="flex-auto flex gap-2">
              <div className="flex-auto">
                <ChatterBox />
              </div>
              <div className="flex-shrink">
                <StaffList />
              </div>
            </div>

          </div>
          <div className='flex-auto m-2 flex flex-col justify-between' style={{ "width": "50%" }}>
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
