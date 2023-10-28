import React from 'react';
import PerceptionList from './PerceptionList';

const PatientTest: React.FC = () => {
    return (
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100vh' }}>
            <div className="w-1/6 h-1/2">
                <PerceptionList />
            </div>
        </div>
    );
};

export default PatientTest;