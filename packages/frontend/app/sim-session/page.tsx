"use client"

import React from 'react';
import { StaffDefinition } from './StaffCard';
import ChatterBox from '../chatter/page';
import "./page.css"
import DrClippySuggestions from './DrClippy/DrClippy';
import StaffList from './StaffList/StaffList';
import PatientVisualization from './Patient/PatientVisualization';
import { ActionLog } from './ActionLog/ActionLog';
import TimeDisplay from './TimeDisplay/TimeDisplay';
import { Objective, LearnerActionsList } from './LearnerActions/LearnerActionsList';
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
        <div className='page-container pl-2 pr-2 pb-2'>
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
              <div className="flex-auto flex flex-grow overflow-hidden h-full gap-2">
                <div className="flex-auto">
                  <ChatterBox />
                </div>
                <div className="flex-shrink">
                  <StaffList />
                </div>
              </div>

            </div>
            <div className='column w-1/6 gap-2' style={{ flex: "0 1 auto" }}>
              <LearnerActionsList objectives={objectives} />
              <div className="self-end w-full">
                <DrClippySuggestions onClick={(data) => { handleClippySuggestion(data) }} />
              </div>
            </div>

          </div>
        </div>
      </APIProvider>
    </SocketProvider>

  );
}

export default SimSessionPage;
