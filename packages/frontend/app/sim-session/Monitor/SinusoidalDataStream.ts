import { Observable } from 'rxjs';


const fps = 30;
const frameInterval = 1000 / fps;

export class SinusoidalDataStream {
  private dataStream: Observable<number[]>;
  private currentBPM: number;
  private currentlyConnected: boolean = false;
  private time: number = 0;


  constructor() {
    this.currentBPM = 60;
    this.dataStream = this.createDataStream();
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

  private createDataStream(): Observable<number[]> {
    return new Observable<number[]>(subscriber => {
      let index = 0;

      const emitData = () => {
        if (!this.currentlyConnected) {
          return;
        }

        const frequency = this.currentBPM / 60;
        const angularFrequency = 2 * Math.PI * frequency;

        const phase = angularFrequency * this.time;

        const sineValueStandard = Math.sin(phase);
        const offset = (Math.cos(this.time / 0.37) + 1)* 0.02;

        const sineValueSkewed = Math.sin(phase + (sineValueStandard * offset * angularFrequency));
  
        // Emit the skewed sine value through the stream
        subscriber.next([sineValueSkewed]);
  
        // Increment the time by a fraction, similar to before.
        this.time += (frameInterval / 1000) * (Math.random() * 0.1 + 0.95);
      };

      const intervalId = setInterval(emitData, frameInterval);

      return () => {
        clearInterval(intervalId);
      };
    });
  }
}
