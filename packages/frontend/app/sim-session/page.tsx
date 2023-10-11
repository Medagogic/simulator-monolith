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
import StaffList, { StaffMemberData } from './StaffList/StaffList';
import BedVisualization from './BedVisualization';


const staffData: StaffDefinition[] = [
  { name: 'Dr. Smith', role: 'Doctor', activity: 'Checking vitals' },
  { name: 'Jane Doe', role: 'Nurse', activity: 'Administering medication' },
  { name: 'John Doe', role: 'Anaesthetist', activity: 'Monitoring anesthesia' },
  { name: 'Dr. Pooper', role: 'Doctor', activity: 'Checking vitals' },
  { name: 'Jane Doe', role: 'Nurse' },
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
    <div style={{ width: "100%", height: "100%" }} className='flex flex-col base'>
      <div className='toolbar prose' style={{ maxWidth: "100%" }}>
        <h1 className="text-white">
          Medagogic Simulator
        </h1>
      </div>
      <div style={{ "width": "100%", "height": "100%" }} className='flex flex-row'>
        <div className='flex flex-col flex-auto gap-2 m-2' style={{ "width": "100%" }}>
          <VitalSignsDisplay vitalSigns={vitalSigns} />
          {/* <EmergencyRoomVisualization staff={staffData} /> */}
          <div className="flex gap-2">
            <div className="flex-auto">
              <BedVisualization/>
            </div>
            <div className="flex-auto">
              <ABCDEList abcdeData={abcdeData} vitalSigns={vitalSigns} />
            </div>
          </div>
          
        </div>
        <div className='flex-auto m-2 flex flex-col gap-2' style={{ "width": "100%" }}>
          <div className="flex-auto flex gap-2">
            <div className="chatterbox flex-auto">
              <ChatterBox messages={messages} />
            </div>
            <div className="flex-shrink">
              <StaffList staffData={getStaffData()} />
            </div>
          </div>
          <Clippy onClick={(data) => { handleClippySuggestion(data) }} /> 
        </div>
      </div>
    </div>
  );
}

export default SimSessionPage;
