"use client"

import React from 'react';
import { StaffDefinition } from './StaffCard';
import EmergencyRoomVisualization from './EmergencyRoomVisualization';
import VitalSignsDisplay from './VitalSignsDisplay';
import { FullVitalSigns } from '@/src/api';
import ChatterBox, { Message } from '../chatter/page';
import "./page.css"


const staffData: StaffDefinition[] = [
  { name: 'Dr. Smith', role: 'Doctor', activity: 'Checking vitals' },
  { name: 'Jane Doe', role: 'Nurse', activity: 'Administering medication' },
  { name: 'John Doe', role: 'Anaesthetist', activity: 'Monitoring anesthesia' },
  { name: 'Dr. Pooper', role: 'Doctor', activity: 'Checking vitals' },
  { name: 'Jane Doe', role: 'Nurse', activity: 'Administering medication' },
];

const vitalSigns: FullVitalSigns = {
  temperature: '98.6 °C',
  heartRate: '75 bpm',
  respiratoryRate: '16 bpm',
  bloodPressure: '120/80 mmHg',
  bloodGlucose: '90 mg/dL',
  oxygenSaturation: '98%',
  capillaryRefill: '<2 seconds'
};

const messages: Message[] = [{ text: "Hello", sender: "user", date: new Date() }];


const SimSessionPage: React.FC = () => {

  return (
    <div style={{ "width": "100%", "height": "100%" }} className='flex flex-col'>
      <div className='toolbar'>Toolbar</div>
      <div style={{ "width": "100%", "height": "100%" }} className='flex flex-row'>
        <div className='flex flex-col flex-auto' style={{ "width": "100%" }}>
          <VitalSignsDisplay vitalSigns={vitalSigns} />
          <EmergencyRoomVisualization staff={staffData} />
          <div>Footer</div>
        </div>
        <div className='flex-auto chatterbox-outer' style={{ "width": "100%" }}>
          <ChatterBox messages={messages}/>
        </div>
      </div>
    </div>
  );
}

export default SimSessionPage;
