// components/VitalSignsDisplay.tsx

import { FullVitalSigns } from '@/src/api';
import React from 'react';
import "./VitalSignsDisplay.css"

interface Props {
    vitalSigns: FullVitalSigns;
}


const VitalSignItem: React.FC<{ label: string, value: string, color?: string }> = ({ label, value, color = "text-white" }) => {
    return (
        <div className="flex flex-col items-center">
            <span className={`text-xs uppercase ${color}`}>{label}</span>
            <span className="text-sm font-bold">{value}</span>
        </div>
    );
};

const VitalSignsDisplay: React.FC<Props> = ({ vitalSigns }) => {
    return (
        <div className="flex justify-between p-2 text-white shadow-lg w-full vitals-container">
            <VitalSignItem label="Temp" value={vitalSigns.temperature} />
            <VitalSignItem label="Heart Rate" value={vitalSigns.heartRate} color="text-red-500" />
            <VitalSignItem label="Resp Rate" value={vitalSigns.respiratoryRate} />
            <VitalSignItem label="BP" value={vitalSigns.bloodPressure} />
            <VitalSignItem label="Glucose" value={vitalSigns.bloodGlucose} />
            <VitalSignItem label="O2 Sat" value={vitalSigns.oxygenSaturation} color="text-blue-500" />
            <VitalSignItem label="Cap Refill" value={vitalSigns.capillaryRefill} />
        </div>
    );
};

export default VitalSignsDisplay;