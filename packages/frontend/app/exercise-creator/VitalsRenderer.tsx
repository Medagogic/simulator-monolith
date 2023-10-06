import React from 'react';
import { VitalSigns, vitalSignsLabels } from './ExerciseTypes';

type VitalsRendererProps = {
    vitalData: VitalSigns;
    onChange: (key: keyof VitalSigns, value: string) => void;
};

const VitalsRenderer: React.FC<VitalsRendererProps> = ({ vitalData, onChange }) => {
    return (
        <div>
            {Object.entries(vitalData).map(([key, value]) => (
                <div key={key} style={{display: "flex", gap: "0.5rem"}}>
                    <strong>{vitalSignsLabels[key as keyof VitalSigns]}:</strong>
                    <input
                        style={{flexGrow: 1}}
                        type="text"
                        value={value ?? ''}
                        onChange={(e) => onChange(key as keyof VitalSigns, e.target.value)}
                    />
                </div>
            ))}
        </div>
    );
};

export default VitalsRenderer;
