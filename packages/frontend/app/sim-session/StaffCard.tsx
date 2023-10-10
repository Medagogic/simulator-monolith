import React from 'react';
import "./StaffCard.css"

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
        <div className="flex flex-col items-center cursor-pointer hover:shadow-lg">
            <div className="bg-white w-16 h-16 rounded-full border border-blue-200 shadow-md" style={{transform: "translate(0px, 3px)"}}></div>
            <div className="border border-blue-200 shadow-md p-1 bg-white w-36 torso" title={definition.name} onClick={onClick}
            style={{borderTopLeftRadius: "2rem", borderTopRightRadius: "2rem"}}>
                <div className="flex items-center mb-1">
                    {getRoleSymbol()}
                    <div className="font-bold text-sm whitespace-nowrap truncate max-w-xs">{definition.name}</div>
                </div>
                <div className="bg-blue-100 p-0.5 rounded-md">
                    <span className="text-blue-700 text-xs">{definition.activity}</span>
                </div>
            </div>
        </div>
    );
};

export default StaffCard;
