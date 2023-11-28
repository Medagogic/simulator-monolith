"use client"

import React from 'react';
import ChatterBox from '../chatter/page';
import "./page.css"
import DrClippySuggestions from './DrClippy/DrClippy';
import StaffList from './StaffList/StaffList';
import PatientVisualization from './Patient/PatientVisualization';
import { ActionLog } from './ActionLog/ActionLog';
import TimeDisplay from './TimeDisplay/TimeDisplay';
import { LearnerActionsList } from './LearnerActions/LearnerActionsList';
import PatientMonitor from './Monitor/PatientMonitor';
import { useSessionStore } from '../storage/SessionStore';
import BriefingModal from './Briefing/BriefingModal';


export interface SimSessionPageProps {

}


const SimSessionPage: React.FC<SimSessionPageProps> = ({ }) => {
  const sessionName = useSessionStore((state) => state.sessionName);
  const [showBriefingModal, setShowBriefingModal] = React.useState(true);

  function closeBriefingModal() {
    setShowBriefingModal(false);
  }

  function handleClippySuggestion(data: { description: string, command: string }) {
    console.log(data.command);
  }

  return (
    <div className='page-container pl-2 pr-2 pb-2'>
      <BriefingModal isOpen={showBriefingModal} onClose={closeBriefingModal}/>

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
            {/* <div className="flex-shrink">
              <StaffList />
            </div> */}
          </div>

        </div>
        <div className='column w-1/6 gap-2' style={{ flex: "0 1 auto" }}>
          <LearnerActionsList />
          <div className="self-end w-full">
            <DrClippySuggestions onClick={(data) => { handleClippySuggestion(data) }} />
          </div>
        </div>

      </div>
    </div>

  );
}

export default SimSessionPage;
