import React from 'react';
import "./StaffList.css";

// Data structure for staff member
export interface StaffMemberData {
  id: string; // Unique identifier
  name: string;
  specialty: string;
  activity?: string; // e.g. "Assisting Patient", "Reviewing Charts", null for "Idle"
}

// StaffMember component
interface StaffMemberProps {
  data: StaffMemberData;
}

const StaffMember: React.FC<StaffMemberProps> = ({ data }) => {
  return (
    <div className="bg-gray-700 rounded-md shadow-md space-y-2 text-white staff-member-container">
      <div className="staff-info"> {/* New container div for name and specialty */}
        <h2 className="text-xl font-bold mr-4 staff-member-name">{data.name}</h2>
        <p className="text-sm font-semibold staff-member-specialty">{data.specialty}</p>
      </div>
      <div className="activity-indicator" style={{ backgroundColor: data.activity ? "green" : "#ff080854" }}>
        {data.activity || "Inactive"}
      </div>
    </div>
  );
};

// StaffList component
interface StaffListProps {
  staffData: StaffMemberData[];
}

const StaffList: React.FC<StaffListProps> = ({ staffData }) => {
  return (
    <div className="staff-list">
      {staffData.map(staff => (
        <StaffMember key={staff.id} data={staff} />
      ))}
    </div>
  );
};

export default StaffList;
