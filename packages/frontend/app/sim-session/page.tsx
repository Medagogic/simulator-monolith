"use client"

import React from 'react';
import { StaffDefinition } from './StaffCard';
import EmergencyRoomVisualization from './EmergencyRoomVisualization';
import VitalSignsDisplay from './VitalSignsDisplay';
import { FullABCDE, FullVitalSigns } from '@/src/api';
import ChatterBox, { Message } from '../chatter/page';
import "./page.css"
import Clippy from './clippy/Clippy';
import ABCDEList from './ABCDEList/ABCDEList';


const staffData: StaffDefinition[] = [
  { name: 'Dr. Smith', role: 'Doctor', activity: 'Checking vitals' },
  { name: 'Jane Doe', role: 'Nurse', activity: 'Administering medication' },
  { name: 'John Doe', role: 'Anaesthetist', activity: 'Monitoring anesthesia' },
  { name: 'Dr. Pooper', role: 'Doctor', activity: 'Checking vitals' },
  { name: 'Jane Doe', role: 'Nurse', activity: 'Administering medication' },
];

const vitalSigns: FullVitalSigns = {
  temperature: '38.6 °C',
  heartRate: '75 bpm',
  respiratoryRate: '16 bpm',
  bloodPressure: '120/80 mmHg',
  bloodGlucose: '90 mg/dL',
  oxygenSaturation: '98%',
  capillaryRefill: '<2 seconds'
};

const abcdeData: FullABCDE = {
  a: 'Airway patent.',
  b: 'Laboured breathing, right chest pain.',
  c: 'Tachycardic.',
  d: 'AVPU: A',
  e: 'No external bleeding or rashes.',
};

const messages: Message[] = [{ text: "Hello", sender: "user", date: new Date() }];


const SimSessionPage: React.FC = () => {

  function handleClippySuggestion(data: {description: string, command: string}) {
    console.log(data.command);
  }

  return (
    <div style={{ width: "100%", height: "100%" }} className='flex flex-col base'>
      <div className='toolbar prose' style={{maxWidth: "100%"}}>
        <h1 className="text-white">
          Medagogic Simulator
        </h1>
      </div>
      <div style={{ "width": "100%", "height": "100%" }} className='flex flex-row'>
        <div className='flex flex-col flex-auto' style={{ "width": "100%" }}>
          <VitalSignsDisplay vitalSigns={vitalSigns} />
          <EmergencyRoomVisualization staff={staffData} />
        </div>
        <div className='flex-auto chatterbox-outer flex flex-col' style={{ "width": "100%" }}>
          <div className='flex flex-row'>
          <ABCDEList abcdeData={abcdeData} vitalSigns={vitalSigns} />
            <Clippy onClick={(data) => {handleClippySuggestion(data)}} />
          </div>
          <div className="chatterbox flex-auto">
            <ChatterBox messages={messages}/>
          </div>
        </div>
      </div>
    </div>
  );
}

export default SimSessionPage;
