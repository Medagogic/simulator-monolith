import { Observable } from 'rxjs';

export const createSinusoidalDataStream = (frequency: number = 1, skewFactor: number = 2) => {
  // Ensure skewFactor is valid to avoid unexpected behavior
  if (skewFactor < 1) {
    throw new Error('skewFactor must be greater than or equal to 1');
  }

  return new Observable<number[]>(subscriber => {
    let time = 0;
    const intervalPeriod = 100;
    const angularFrequency = 2 * Math.PI * frequency;

    const intervalId = setInterval(() => {
      const phase = angularFrequency * time;

      const sineValueStandard = Math.sin(phase + 0.2);

      const sineValueSkewed = Math.sin(phase + (sineValueStandard * 0.1 * angularFrequency));

      // Emit the skewed sine value through the stream
      subscriber.next([sineValueSkewed]);

      // Increment the time by a fraction, similar to before.
      time += intervalPeriod / 1000;

    }, intervalPeriod);

    // Clear interval and end the data stream properly when it's no longer used
    return () => clearInterval(intervalId);
  });
};
