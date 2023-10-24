"use client"

import React from 'react';
import { ExerciseCreationABCDE, ExerciseCreationVitalSigns } from '@/src/api';
import { VitalSigns } from '@/src/scribe/scribetypes';
import "../page.css"
import PatientVisualization from '../Patient/PatientVisualization';
import { ActionLog, ActionLogEntry } from '../ActionLog/ActionLog';
import TimeDisplay from '../TimeDisplay/TimeDisplay';
import { Objective, ObjectivesList } from '../ObjectivesList/ObjectivesList';
import { SocketProvider, useSocket } from '../../socketio/SocketContext';
import PatientMonitor from '../Monitor/PatientMonitor';
import DirectInput from './DirectInput';

import action_definitions from "../../../../medagogic_sim/action_definitions.json";
import FunctionSelector, { FunctionDefinition } from './FunctionSelector';

import {EmitEvent} from "@/src/scribe/ScribeClient";



const vitalSignsForABCDEList: ExerciseCreationVitalSigns = {
  temperature: '38.6 °C',
  heartRate: '75 bpm',
  respiratoryRate: '16 bpm',
  bloodPressure: '120/80 mmHg',
  bloodGlucose: '90 mg/dL',
  oxygenSaturation: '98%',
  capillaryRefill: '<2 seconds'
};

const vitalSignsForDisplay: VitalSigns = {
  temperature: 38.6,
  heart_rate: 75,
  respiratory_rate: 16,
  blood_pressure: { systolic: 120, diastolic: 80 },
  blood_glucose: 90,
  oxygen_saturation: 98,
  capillary_refill: 2
};

const abcdeData: ExerciseCreationABCDE = {
  a: 'Airway patent.',
  b: 'Laboured breathing, right chest pain.',
  c: 'Tachycardic.',
  d: 'AVPU: A',
  e: 'No external bleeding or rashes.',
};

const actionLogs: ActionLogEntry[] = [
  // { timestamp: new Date(), staffName: 'Aragon', action: 'assess capillary refill time', actionType: ActionType.Assessment },
  // { timestamp: new Date(), staffName: 'Gandalf', action: 'obtained IV access', actionType: ActionType.Intervention },
  // { timestamp: new Date(), staffName: 'Merry', action: 'called for xray prep', actionType: ActionType.Communication },
  // { timestamp: new Date(), staffName: 'Pippin', action: 'prepared 1L of saline', actionType: ActionType.Preparation },
];

const objectives: Objective[] = [
  { description: 'Assess airway as priority.', completed: true },
  { description: 'Resolve airway obstruction.', completed: false },
  { description: 'Administer 50mg medication A.', completed: true },
  // ... other objectives
];


function parseFunctionDefinition(input: string): FunctionDefinition {
  const regex = /\$([a-zA-Z_]\w*)/g;
  const params: string[] = [];
  let match;

  while ((match = regex.exec(input)) !== null) {
      params.push(match[1]);
  }

  // Remove the parameters from the original string
  const function_name = input.replace(/\(\$[a-zA-Z_]\w*(, ?\$[a-zA-Z_]\w*)*\)/, '').trim();

  return {
    function_name,
      params
  };
}

const function_definitions = action_definitions.map((action) => {
  return parseFunctionDefinition(action.name);
});
console.log(function_definitions);



export const DirectSimulation: React.FC = () => {
  const socket = useSocket();

  function sendIntervention(message: string) {
    console.log("sendIntervention: " + message);
  }

  function onSubmitFunction(function_call: string) {
    console.log("onSubmitFunction: " + function_call);
    socket!.emit(EmitEvent.DIRECT_INTERVENTION, function_call);
  }


  return (
      <div style={{ width: "100%", height: "100%" }} className='flex flex-col base'>
        <div className='toolbar' style={{ maxWidth: "100%", display: 'flex', flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' }}>
          <div style={{ flex: 1 }}>
            Medagogic Simulator
          </div>

          <div style={{ display: 'flex', justifyContent: 'center', position: 'absolute', left: 0, right: 0 }}>
            <TimeDisplay />
          </div>

          <div style={{ flex: 1, display: 'flex', justifyContent: 'flex-end' }}>
            <h1 className="text-white">

            </h1>
          </div>
        </div>

        <div style={{ "width": "100%", "height": "100%" }} className='flex flex-row'>
          <div className='flex flex-col flex-auto gap-2 m-2' style={{ width: "100%", height: "100%" }}>
            <PatientVisualization />
            <PatientMonitor />
          </div>

          <div className='flex-auto m-2 flex flex-col gap-2' style={{ "width": "100%" }}>
            <div>
              <ActionLog logs={actionLogs} />
            </div>
{/* 
            <div>
              <DirectInput onSubmit={sendIntervention} />
            </div> */}

            <div>
              <FunctionSelector functions={function_definitions} onSubmit={onSubmitFunction} />
            </div>

          </div>
          <div className='flex-auto m-2 flex flex-col justify-between' style={{ "width": "50%" }}>
            <ObjectivesList objectives={objectives} />
          </div>

        </div>
      </div>
  );
}


const DirectSimulationContainer: React.FC = () => {
  return (
    <SocketProvider session_id='default-session'>
      <DirectSimulation />
    </SocketProvider>
  );
}


export default DirectSimulationContainer;
