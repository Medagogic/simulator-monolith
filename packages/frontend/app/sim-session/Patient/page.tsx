import React from 'react';
import PatientVisualization from './PatientVisualization';

const PatientTest: React.FC = () => {
    return (
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100vh' }}>
            <div className="w-1/3 h-1/2">
                <PatientVisualization />
            </div>
        </div>
    );
};

export default PatientTest;