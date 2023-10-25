"use client"

import React, { useEffect } from 'react';
import "./StaffList.css";
import { sessionRequestParams, useAPI } from '@/app/socketio/APIContext';
import { APINPCData, APITeamData } from '@/src/api';


// StaffMember component
interface StaffMemberProps {
  data: APINPCData;
}

const StaffMember: React.FC<StaffMemberProps> = ({ data }) => {
  return (
    <div className="bg-gray-700 rounded-md shadow-md space-y-2 text-white staff-member-container">
      <div className="staff-info"> {/* New container div for name and specialty */}
        <h2 className="text-xl font-bold mr-4 staff-member-name">{data.definition.name}</h2>
        <p className="text-sm font-semibold staff-member-specialty">{data.definition.role}</p>
      </div>
      <div className="activity-indicator" style={{ backgroundColor: data.currentTask ? "green" : "#ff080854" }}>
        {data.currentTask || "Inactive"}
      </div>
    </div>
  );
};

// StaffList component
interface StaffListProps {
  
}

const StaffList: React.FC<StaffListProps> = ({  }) => {
  const api = useAPI();
  const requestParams = sessionRequestParams();
  
  const [staffData, setStaffData] = React.useState<APINPCData[]>([]);
  let loading = false;

  useEffect(() => {
    if (loading) {
      return;
    }
    loading = true;

    api.medsimTeamNewSessionRouterSessionSessionIdMedsimTeamGet(
      requestParams,
    ).then((response: APITeamData) => {
      response.npcData.forEach((npc: APINPCData) => {
        setStaffData(staffData => [...staffData, npc]);
      });
    });
  }, []);

  return (
    <div className="staff-list">
      {staffData.map(staff => (
        <StaffMember key={staff.id} data={staff} />
      ))}
    </div>
  );
};

export default StaffList;
