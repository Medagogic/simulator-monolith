// components/VitalSignsDisplay.tsx

import { FullVitalSigns } from '@/src/api';
import React from 'react';
import "./VitalSignsDisplay.css"

interface Props {
    vitalSigns: FullVitalSigns;
}

const VitalSignItem: React.FC<{ label: string, value: string | null, color?: string }> = ({ label, value, color = "text-white" }) => {
    // Check if the value is null and display "Disconnected" if it is
    const displayValue = value !== null ? value : "N/A";
    const displayColor = value !== null ? color : "text-gray-500"; // Change color if disconnected
    const valueColor = value !== null ? "text-white" : "text-gray-500"; // Change color if disconnected

    return (
        <div className="flex flex-col items-center">
            <span className={`text-xs uppercase ${displayColor}`}>{label}</span>
            <span className={`text-sm font-bold ${valueColor}`}>{displayValue}</span>
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
