import { FullVitalSigns } from "@/src/api";
import { ReactNode } from "react";
import "./ABCDECards.css";


interface CardContainerProps {
    children: ReactNode;
    title: string;
    description: string;
}

interface VitalSignProps {
    label: string;
    value: string | null;
    color?: string;
}

const CardContainer: React.FC<CardContainerProps> = ({ children, title, description }) => {
    return (
        <div className="bg-gray-700 rounded-md shadow-md space-y-2 text-white abcde-card-container">
            <div className="flex items-center">
                <h2 className="text-xl font-bold mr-4 abcde-card-title">{title}</h2>
                <div className="flex-grow">
                <p className="mb-1 text-white text-sm font-semibold">{description}</p>
                    {children}
                </div>
            </div>
        </div>
    );
};

const VitalSignItem: React.FC<VitalSignProps> = ({ label, value, color = "text-white" }) => {
    const displayValue = value !== null ? value : "N/A";
    const valueColor = value !== null ? color : "text-gray-500";
    return (
        <span className={`inline-block rounded-full px-3 py-1 text-xs font-semibold bg-gray-600 ${valueColor}`}>{label}: {displayValue}</span>
    );
};

export const ACard: React.FC<{ description: string; vitalSigns: FullVitalSigns }> = ({ description, vitalSigns }) => {
    return (
        <CardContainer title="A" description={description}>
        </CardContainer>
    );
};


export const BCard: React.FC<{ description: string; vitalSigns: FullVitalSigns }> = ({ description, vitalSigns }) => {
    return (
        <CardContainer title="B" description={description}>
            <div className="vitals-chips-container">
                <VitalSignItem label="Resp Rate" value={vitalSigns.respiratoryRate} />
                <VitalSignItem label="O2 Sat" value={vitalSigns.oxygenSaturation} color="text-blue-500" />
            </div>
        </CardContainer>
    );
};

export const CCard: React.FC<{ description: string; vitalSigns: FullVitalSigns }> = ({ description, vitalSigns }) => {
    return (
        <CardContainer title="C" description={description}>
            <div className="vitals-chips-container">
                <VitalSignItem label="Heart Rate" value={vitalSigns.heartRate} color="text-red-500" />
                <VitalSignItem label="BP" value={vitalSigns.bloodPressure} />
                <VitalSignItem label="Cap Refill" value={vitalSigns.capillaryRefill} />
            </div>
        </CardContainer>
    );
};

export const DCard: React.FC<{ description: string; vitalSigns: FullVitalSigns }> = ({ description, vitalSigns }) => {
    return (
        <CardContainer title="D" description={description}>
            <div className="vitals-chips-container">
                <VitalSignItem label="Glucose" value={vitalSigns.bloodGlucose} />
            </div>
        </CardContainer>
    );
};

export const ECard: React.FC<{ description: string; vitalSigns: FullVitalSigns }> = ({ description, vitalSigns }) => {
    return (
        <CardContainer title="E" description={description}>
            <div className="vitals-chips-container">
                <VitalSignItem label="Temp" value={vitalSigns.temperature} />
            </div>
        </CardContainer>
    );
};