// components/VitalSignsDisplay.tsx
"use client"

import { DefaultApi, Configuration } from '@/src/api';
import { VitalSigns } from '@/src/scribe/scribetypes';
import React, { useEffect } from 'react';
import "./VitalSignsDisplay.css"
import { PatientIO } from '../socketio/PatientIO';
import { useSocket } from '../socketio/SocketContext';
import { usePatientStore } from './Patient/PatientStore';

interface Props {
    debugVitalSigns: VitalSigns;
}

const api = new DefaultApi(new Configuration({ basePath: "http://localhost:5000" }));

const VitalSignItem: React.FC<{ label: string, value: string | null, color?: string }> = ({ label, value, color = "text-white" }) => {
    // Check if the value is null and display "Disconnected" if it is
    const displayValue = value !== null ? value : "N/A";
    const displayColor = value !== null ? color : "text-gray-500"; // Change color if disconnected
    const valueColor = value !== null ? "text-white" : "text-gray-500"; // Change color if disconnected

    return (
        <div className="flex flex-col items-center">
            <span className={`text-xs uppercase ${displayColor}`}>{label}</span>
            <span className={`text-sm font-bold ${valueColor} blinking`}>{displayValue}</span>
        </div>
    );
};

const VitalSignsDisplay: React.FC<Props> = ({ debugVitalSigns }) => {
    const [patientIO, setPatientIO] = React.useState<PatientIO | null>(null);
    const vitalSigns = usePatientStore((state) => state.vitals);

    const socket = useSocket();
    useEffect(() => {
        if (socket) {
            socket.on("connect", () => {
                console.log("VitalSignsDisplay: socket connected");
            });
            const newPatientIO = new PatientIO(socket);
            setPatientIO(newPatientIO);
        }
    }, [socket]);

    return (
        <div className="flex justify-between p-2 text-white shadow-lg w-full vitals-container">
            {vitalSigns != null &&
                <>
                    <VitalSignItem label="Temp" value={`${vitalSigns.temperature.toFixed(2)}°C`} />
                    <VitalSignItem label="Heart Rate" value={`${vitalSigns.heart_rate.toFixed(0)} BPM`} color="text-red-500" />
                    <VitalSignItem label="Resp Rate" value={`${vitalSigns.respiratory_rate.toFixed(0)} BPM`} />
                    <VitalSignItem label="BP" value={`${vitalSigns.blood_pressure.systolic.toFixed(0)}/${vitalSigns.blood_pressure.diastolic.toFixed(0)}`} />
                    <VitalSignItem label="Glucose" value={`${vitalSigns.blood_glucose.toFixed(0)} mg/dL`} />
                    <VitalSignItem label="O2 Sat" value={`${vitalSigns.oxygen_saturation.toFixed(1)}%`} color="text-blue-500" />
                    <VitalSignItem label="Cap Refill" value={`${vitalSigns.capillary_refill.toFixed(1)} sec`} />
                </>
            }
        </div>
    );
    
};

export default VitalSignsDisplay;
