"use client"

import React, { useEffect, useState } from 'react';
import { DummyDataStream } from './DummyDataStream';
import SmoothieGraph from './SmoothieGraph';
import { createSinusoidalDataStream } from './SinusoidalDataStream';
import { VitalSigns } from '@/src/scribe/scribetypes';
import { usePatientStore } from '../Patient/PatientStore';
import { usePatientIO } from '@/app/socketio/SocketContext';


const PatientMonitor: React.FC = () => {
  const vitalSigns = usePatientStore((state) => state.vitals);
  const patientIO = usePatientIO();

  const [datastream_ecg, setDatastream_ecg] = useState<DummyDataStream>(new DummyDataStream('ecg'));
  const [datastream_bp, setDatastream_bp] = useState<DummyDataStream>(new DummyDataStream('bloodPressure'));
  const [datastream_breath, setDatastream_breath] = useState(createSinusoidalDataStream());
  const [datastream_spo2, setDatastream_spo2] = useState<DummyDataStream>(new DummyDataStream('bloodPressure'));

  const chartWidth = 400;
  const chartHeight = 100;

  useEffect(() => {
    if (vitalSigns) {
      // console.log("PatientMonitor: new vitals", vitalSigns);
      const bpm = vitalSigns.heart_rate;
      datastream_ecg.updateBpm(bpm);
      datastream_bp.updateBpm(bpm);
      datastream_spo2.updateBpm(bpm);
    }
  }, [vitalSigns]);


  function heartRate() {
    if (vitalSigns) {
      return vitalSigns.heart_rate.toFixed(0);
    } else {
      return "";
    }
  }

  function bloodPressure() {
    if (vitalSigns) {
      return `${vitalSigns.blood_pressure.systolic.toFixed(0)}/${vitalSigns.blood_pressure.diastolic.toFixed(0)}`;
    } else {
      return "";
    }
  }

  function respRate() {
    if (vitalSigns) {
      return vitalSigns.respiratory_rate.toFixed(0);
    } else {
      return "";
    }
  }

  function spo2() {
    if (vitalSigns) {
      return vitalSigns.oxygen_saturation.toFixed(1);
    } else {
      return "";
    }
  }


  return (
    <div>
      <div className='bg-black text-white flex flex-row leading-none'>
        <div className='flex flex-col flex-grow'>
          <SmoothieGraph dataStream={datastream_ecg.getDataStream()} width={chartWidth} height={chartHeight} color="#00ff00" millisPerPixel={5} />
          <SmoothieGraph dataStream={datastream_bp.getDataStream()} width={chartWidth} height={chartHeight} color="#ff0000" millisPerPixel={5} />
          <SmoothieGraph dataStream={datastream_breath} width={chartWidth} height={chartHeight} color="#ffff00" millisPerPixel={15} />
          <SmoothieGraph dataStream={datastream_spo2.getDataStream()} width={chartWidth} height={chartHeight} color="#00ffff" millisPerPixel={5} />
        </div>
        <div className='flex flex-col w-48 gap-2 p-2'>
          <div className='flex flex-col' style={{ color: "#00ff00" }}>
            <div className='flex place-content-between'>
              <div className='font-bold'>
                ECG
              </div>
              <div className='font-light'>
                BPM
              </div>
            </div>
            <div style={{ fontSize: "4rem", fontWeight: "bolder" }}>{heartRate()}</div>
          </div>
          <div className='flex flex-col pt-2' style={{ color: "#ff0000" }}>
            <div className='flex place-content-between'>
              <div className='font-bold'>
                BP
              </div>
              <div className='font-light'>
                mmHg
              </div>
            </div>
            <div style={{ fontSize: "3rem", fontWeight: "bolder" }}>{bloodPressure()}</div>
          </div>
          <div className='flex flex-col pt-8' style={{ color: "#ffff00" }}>
            <div className='flex place-content-between'>
              <div className='font-bold'>
                Resp
              </div>
              <div className='font-light'>
                Breaths/Min
              </div>
            </div>
            <div style={{ fontSize: "3rem", fontWeight: "bolder" }}>{respRate()}</div>
          </div>
          <div className='flex flex-col pt-8' style={{ color: "#00ffff" }}>
            <div className='flex place-content-between'>
              <div className='font-bold'>
                SpO<span style={{ verticalAlign: "sub" }}>2</span>
              </div>
              <div className='font-light'>
                %
              </div>
            </div>
            <div style={{ fontSize: "3rem", fontWeight: "bolder" }}>{spo2()}</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PatientMonitor;
