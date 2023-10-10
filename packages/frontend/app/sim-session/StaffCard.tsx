// components/StaffCard.tsx

import React from 'react';

export type StaffDefinition = {
    name: string;
    role: 'Doctor' | 'Nurse' | 'Anaesthetist';
    activity: string;
};

type StaffCardProps = {
    definition: StaffDefinition;
    onClick?: () => void;
};

const StaffCard: React.FC<StaffCardProps> = ({ definition, onClick }) => {
    // Selecting symbol based on role
    const getRoleSymbol = () => {
        switch(definition.role) {
            case 'Doctor':
                return <span className="bg-blue-600 text-white rounded-full w-6 h-6 flex items-center justify-center mr-2" title="Doctor">D</span>;
            case 'Nurse':
                return <span className="bg-green-600 text-white rounded-full w-6 h-6 flex items-center justify-center mr-2" title="Nurse">N</span>;
            case 'Anaesthetist':
                return <span className="bg-purple-600 text-white rounded-full w-6 h-6 flex items-center justify-center mr-2" title="Anaesthetist">A</span>;
            default:
                return null;
        }
    };

    return (
        <div className="border border-blue-200 rounded-lg shadow-md p-1 bg-white w-36 cursor-pointer hover:shadow-lg" title={definition.name} onClick={onClick}> {/* Updated classes here */}
            <div className="flex items-center mb-1">
                {getRoleSymbol()}
                <div className="font-bold text-sm whitespace-nowrap truncate max-w-xs">{definition.name}</div>
            </div>
            <div className="bg-blue-100 p-0.5 rounded-md">
                <span className="text-blue-700 text-xs">{definition.activity}</span>
            </div>
        </div>
    );
};

export default StaffCard;