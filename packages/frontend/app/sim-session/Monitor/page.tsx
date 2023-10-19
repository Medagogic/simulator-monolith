"use client"

import React from 'react';
import PatientMonitor from './PatientMonitor';
import { VitalSigns } from '@/src/scribe/scribetypes';

const PatientMonitorTestPage = () => {

  const vitalSignsForDisplay: VitalSigns = {
    temperature: 38.6,
    heart_rate: 75,
    respiratory_rate: 16,
    blood_pressure: { systolic: 120, diastolic: 80 },
    blood_glucose: 90,
    oxygen_saturation: 98,
    capillary_refill: 2
  };

  return (
    <div className='flex justify-center' style={{top: "10rem", position: "relative"}}>
      <PatientMonitor/>
    </div>
  );
};

export default PatientMonitorTestPage;
