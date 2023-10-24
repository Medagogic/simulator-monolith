import { BehaviorSubject, Observable } from 'rxjs';
import { dummyDataSet } from "./medical-data"

type dataKey = 'ecg' | 'bloodPressure' | 'bloodVolume' | 'bloodOxygenation';

const fps = 30;
const dummyDataBPM = 76;
const pointsPerFrame = 1000 / fps;
const frameInterval = 1000 / fps;

export class DummyDataStream {
  private dataStream: Observable<number[]>;
  private currentBPM: number;
  private currentlyConnected: boolean = false;

  constructor(vital: dataKey) {
    this.currentBPM = dummyDataBPM;
    this.dataStream = this.createDataStream(vital);
  }

  public updateBpm(newBpm: number) {
    this.currentBPM = newBpm;
  }

  public setConnected(newConnected: boolean) {
    this.currentlyConnected = newConnected;
  }

  public getDataStream(): Observable<number[]> {
    return this.dataStream;
  }

  private createDataStream(vital: dataKey): Observable<number[]> {
    return new Observable<number[]>(subscriber => {
      let index = 0;
      const dummyData = dummyDataSet[vital];

      const emitData = () => {
        if (!this.currentlyConnected) {
          return;
        }

        const pointsThisFrame = pointsPerFrame * this.currentBPM / dummyDataBPM;
        const startIndex = index;
        const endIndex = Math.floor(index + pointsThisFrame);

        if (endIndex >= dummyData.length) {
          index = endIndex - dummyData.length;
        } else {
          index = endIndex;
        }

        let slice;
        if (endIndex >= dummyData.length) {
          const endSlice = dummyData.slice(startIndex);
          const startSlice = dummyData.slice(0, endIndex - dummyData.length);
          slice = endSlice.concat(startSlice);
          index = endIndex - dummyData.length;
        } else {
          slice = dummyData.slice(startIndex, endIndex);
          index = endIndex;
        }

        const max_val = Math.max(...slice);
        const l = slice.length;
        const all_max = Array(l).fill(max_val);

        subscriber.next(all_max);
      };

      const intervalId = setInterval(emitData, frameInterval);

      return () => {
        clearInterval(intervalId);
      };
    });
  }
}
