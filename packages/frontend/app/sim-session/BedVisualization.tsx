import React from 'react';
import patientImage from './patient.png';
import "./BedVisualization.css"

const BedVisualization: React.FC = () => {
    return (
        <div className="bg-white w-1/4 h-1/2 border rounded-lg bed-container" title="Bed">
            <div className="absolute inset-0 flex items-center justify-center bed">
                <img src={patientImage.src} alt="Patient"/>
            </div>
        </div>
    );
};

export default BedVisualization;