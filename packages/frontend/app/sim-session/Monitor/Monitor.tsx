import React, { useRef, useEffect, useState } from 'react';
import { Observable } from 'rxjs';
import Smoothie from 'smoothie';

interface SmoothieGraphProps {
  dataStream: Observable<number[]>; // This prop will receive the data stream
  width: number;
  height: number;
  color?: string; // Optional prop to customize the line color
}

const SmoothieGraph: React.FC<SmoothieGraphProps> = ({ dataStream, width, height, color = '#ff0000' }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  let smoothieInstance: Smoothie.SmoothieChart | null = null;
  let line: Smoothie.TimeSeries = new Smoothie.TimeSeries();

  useEffect(() => {
    if (canvasRef.current) {
      smoothieInstance = new Smoothie.SmoothieChart({
        millisPerPixel: 20,
        maxValueScale: 1.1,
        minValueScale: 1.1,
        grid: {
          verticalSections: 0,
          strokeStyle: "#ffffff22"
        },
        labels: {
          disabled: true,
        },
      });
      smoothieInstance.streamTo(canvasRef.current);
      smoothieInstance.addTimeSeries(line, {strokeStyle: color, lineWidth: 2, interpolation: 'bezier'});
    }

    return () => {
      smoothieInstance?.stop();
    };
  }, []);


  useEffect(() => {
    // Subscribe to the dummy data stream
    const subscription = dataStream.subscribe(newChunk => {
      newChunk.forEach((value, index) => {
        line.append(Date.now(), value);
      });
    });

    // Unsubscribe and cleanup on component unmount
    return () => {
      if (subscription) {
        subscription.unsubscribe();
      }
    };
  }, []); 

  return (
    <div>
      <canvas ref={canvasRef} width={width} height={height} />
    </div>
  );
};

export default SmoothieGraph;
