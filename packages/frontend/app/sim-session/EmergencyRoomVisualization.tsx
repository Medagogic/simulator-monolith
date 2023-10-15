import React from 'react';
import StaffCard, {StaffDefinition} from './StaffCard';
import BedVisualization from './PatientVisualization';
import "./EmergencyRoomVisualization.css"

type EmergencyRoomVisualizationProps = {
    staff: StaffDefinition[];
};

const EmergencyRoomVisualization: React.FC<EmergencyRoomVisualizationProps> = ({ staff }) => {
    const anesthetist = staff.find(person => person.role === 'Anaesthetist');
    const otherStaff = staff.filter(person => person.role !== 'Anaesthetist');

    return (
        <div className="relative bg-gray-200 p-4 emergency-room-container" style={{"width": "100%", "height": "100%"}} >
            <div className="absolute inset-0 flex items-center justify-center">
                <BedVisualization/>
            </div>
            {/* Staff Positioning */}
            {anesthetist && <div className="absolute top-0 left-1/4 w-1/2 flex justify-center">
                <StaffCard definition={anesthetist} />
            </div>}
            <div className="absolute left-10 top-1/4 w-1/4 h-1/2 flex flex-col justify-between">
                {otherStaff.slice(0, 2).map((person, index) => (
                    <div key={index} className="flex justify-center">
                        <StaffCard definition={person} />
                    </div>
                ))}
            </div>
            <div className="absolute right-10 top-1/4 w-1/4 h-1/2 flex flex-col justify-between">
                {otherStaff.slice(2, 4).map((person, index) => (
                    <div key={index} className="flex justify-center">
                        <StaffCard definition={person} />
                    </div>
                ))}
            </div>
            <div className="absolute bottom-0 left-1/4 w-1/2 flex justify-around">
                {otherStaff.slice(4).map((person, index) => (
                    <div key={index} className="flex justify-center">
                        <StaffCard definition={person} />
                    </div>
                ))}
            </div>
        </div>
    );
};

export default EmergencyRoomVisualization;
