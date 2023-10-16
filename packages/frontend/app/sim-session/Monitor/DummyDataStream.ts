import { Observable } from 'rxjs';

// Assuming dummyData is an array of numbers and the path is correctly specified
const dummyDataSet = require('./medical-data.json');

type dataKey = 'ecg' | 'bloodPressure' | 'bloodVolume' | 'bloodOxygenation';

export const createDummyDataStream = (vital: dataKey) => {
  return new Observable<number[]>(subscriber => {
    let index = 0;
    const chunkSize = 16; // Size of each data chunk
    const dummyData = dummyDataSet[vital];

    const intervalId = setInterval(() => {
      const remainingData = dummyData.length - index;
      const currentChunkSize = remainingData >= chunkSize ? chunkSize : remainingData;

      if (remainingData === 0) {
        index = 0;
      }

      const chunk = dummyData.slice(index, index + currentChunkSize);
      subscriber.next(chunk);

      index += currentChunkSize;

      if (index >= dummyData.length) {
        index = 0; 
      }
    }, chunkSize);

    return () => clearInterval(intervalId);
  });
};
