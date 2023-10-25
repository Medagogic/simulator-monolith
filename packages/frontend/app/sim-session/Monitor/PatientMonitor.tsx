"use client"

import React, { useEffect, useState } from 'react';
import { DummyDataStream } from './DummyDataStream';
import SmoothieGraph from './SmoothieGraph';
import { SinusoidalDataStream } from './SinusoidalDataStream';
import { usePatientStore } from '../../storage/PatientStore';
import { usePatientIO } from '@/app/socketio/SocketContext';


const PatientMonitor: React.FC = () => {
  const vitalSigns = usePatientStore((state) => state.vitals);
  const patientIO = usePatientIO();

  const [datastream_ecg, setDatastream_ecg] = useState<DummyDataStream>(new DummyDataStream('ecg'));
  const [datastream_bp, setDatastream_bp] = useState<DummyDataStream>(new DummyDataStream('bloodPressure'));
  const [datastream_breath, setDatastream_breath] = useState<SinusoidalDataStream>(new SinusoidalDataStream());
  const [datastream_spo2, setDatastream_spo2] = useState<DummyDataStream>(new DummyDataStream('bloodPressure'));

  const chartWidth = 420;
  const chartHeight = 80;

  useEffect(() => {
    if (vitalSigns) {
      datastream_ecg.setConnected(true);
      datastream_bp.setConnected(true);
      datastream_breath.setConnected(true);
      datastream_spo2.setConnected(true);

      const bpm = vitalSigns.heart_rate;
      datastream_ecg.updateBpm(bpm);
      datastream_bp.updateBpm(bpm);
      datastream_spo2.updateBpm(bpm);
      const resp_rate = vitalSigns.respiratory_rate;
      datastream_breath.updateBpm(resp_rate);
    }
  }, [vitalSigns]);


  function heartRate() {
    if (vitalSigns) {
      return vitalSigns.heart_rate.toFixed(0);
    } else {
      return "-";
    }
  }

  function bloodPressure() {
    if (vitalSigns) {
      return `${vitalSigns.blood_pressure.systolic.toFixed(0)}/${vitalSigns.blood_pressure.diastolic.toFixed(0)}`;
    } else {
      return "-/-";
    }
  }

  function respRate() {
    if (vitalSigns) {
      return vitalSigns.respiratory_rate.toFixed(0);
    } else {
      return "-";
    }
  }

  function spo2() {
    if (vitalSigns) {
      return vitalSigns.oxygen_saturation.toFixed(1);
    } else {
      return "-";
    }
  }

  const fast_millis_per_pixel = 10;
  const slow_millis_per_pixel = 25;

  return (
      <div className='bg-black text-white flex flex-row leading-none' style={{height: "320px"}}>
        <div className='flex flex-col flex-grow'>
          <SmoothieGraph dataStream={datastream_ecg.getDataStream()} width={chartWidth} height={chartHeight} color="#00ff00" millisPerPixel={fast_millis_per_pixel} />
          <SmoothieGraph dataStream={datastream_bp.getDataStream()} width={chartWidth} height={chartHeight} color="#ff0000" millisPerPixel={fast_millis_per_pixel} />
          <SmoothieGraph dataStream={datastream_breath.getDataStream()} width={chartWidth} height={chartHeight} color="#ffff00" millisPerPixel={slow_millis_per_pixel} />
          <SmoothieGraph dataStream={datastream_spo2.getDataStream()} width={chartWidth} height={chartHeight} color="#00ffff" millisPerPixel={fast_millis_per_pixel} />
        </div>
        <div className='flex flex-col w-48 gap-2 p-2' style={{transformOrigin: "top left", transform: "scale(0.8)"}}>
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
  );
};

export default PatientMonitor;
