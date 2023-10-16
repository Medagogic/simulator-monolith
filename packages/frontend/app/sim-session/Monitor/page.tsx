"use client"

import React from 'react';
import { createDummyDataStream } from './DummyDataStream';
import SmoothieGraph from './Monitor';

const LiveGraphContainer = () => {
  const ecg = createDummyDataStream('ecg');
  const bloodOxygenation = createDummyDataStream('bloodOxygenation')
  const bloodPressure = createDummyDataStream('bloodPressure');
  const bloodVolume = createDummyDataStream('bloodVolume');

  return (
    <div className='bg-black text-white font-mono'>
      <SmoothieGraph dataStream={ecg} width={400} height={200} color="#ff0000" />
      <SmoothieGraph dataStream={bloodOxygenation} width={400} height={200} color="#0000ff" />
      <SmoothieGraph dataStream={bloodPressure} width={400} height={200} color="#00ff00" />
      <SmoothieGraph dataStream={bloodVolume} width={400} height={200} color="#fff" />
    </div>
  );
};

export default LiveGraphContainer;
