"use client"

import React, { useEffect } from 'react';
import "./StaffList.css";
import { sessionRequestParams, useAPI } from '@/app/socketio/APIContext';
import { APINPCData, APITeamData } from '@/src/api';
import { useTeamStore } from '@/app/storage/TeamStore';
import { useChatStore } from '@/app/storage/ChatStore';


// StaffMember component
interface StaffMemberProps {
  data: APINPCData;
  thinkingAbout: string | null;
  onClick: (npcId: string) => void;
  selected: boolean;
}

const StaffMember: React.FC<StaffMemberProps> = ({ data, thinkingAbout, onClick, selected }) => {

  const getActivityIndicator = (data: APINPCData, thinkingAbout: string | null) => {
    let text = '';
    let className = '';

    if (data.currentTask) {
      text = data.currentTask;
      className = "active";
    } else if (thinkingAbout) {
      text = thinkingAbout;
      className = "thinking";
    } else {
      text = 'Inactive';
      className = "idle";
    }

    return (
      <div className={`activity-indicator ${className}`}>
        {text}
      </div>
    );
  };

  function handleClicked() {
    onClick(data.id);
  }

  return (
    <div onClick={handleClicked} className={`bg-gray-700 rounded-md shadow-md space-y-2 text-white staff-member-container cursor-pointer ${selected ? "selected": ""}`}>
      <div className="staff-info">
        <h2 className="text-xl font-bold mr-4 staff-member-name">{data.definition.name}</h2>
        <p className="text-sm font-semibold staff-member-specialty">{data.definition.role}</p>
      </div>
      {getActivityIndicator(data, thinkingAbout)}
    </div>
  );
};


// StaffList component
interface StaffListProps {

}

const StaffList: React.FC<StaffListProps> = ({ }) => {
  const api = useAPI();
  const requestParams = sessionRequestParams();
  const teamById = useTeamStore((state) => state.teamById);
  const setNPCData = useTeamStore((state) => state.setNPCData);
  const thinkingAboutById = useTeamStore((state) => state.thinkingAbout);
  const setToNPCId = useChatStore((state) => state.setToNPCId);
  const toNPCId = useChatStore((state) => state.toNPCId);

  // const [staffData, setStaffData] = React.useState<APINPCData[]>([]);
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
        // setStaffData(staffData => [...staffData, npc]);
        console.log("Setting teamById", npc.id);
        setNPCData(npc.id, npc);
      });
    }).catch((err: any) => {
      console.log("Error getting team data", err);
    });
  }, []);

  function onStaffMemberClick(npc_id: string) {
    if (npc_id === toNPCId) {
      setToNPCId(undefined);
    } else {
      setToNPCId(npc_id);
    }
  }

  return (
    <div className="staff-list">
      {Object.keys(teamById).map((key) => {
        const npc = teamById[key];
        const thinkingAbout = key in thinkingAboutById ? thinkingAboutById[key] : null;
        return <StaffMember key={npc.id} data={npc} thinkingAbout={thinkingAbout} onClick={onStaffMemberClick} selected={npc.id===toNPCId} />;
      })}
      {/* {staffData.map(staff => (
        <StaffMember key={staff.id} data={staff} />
      ))} */}
    </div>
  );
};

export default StaffList;
