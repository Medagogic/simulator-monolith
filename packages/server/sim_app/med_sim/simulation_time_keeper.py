from abc import ABC, abstractproperty
import asyncio

class ISimulationTimeKeeper(ABC):
    @abstractproperty
    def exerciseTimeSeconds(self) -> float:
        pass


class DummyTimeKeeper(ISimulationTimeKeeper):
    def __init__(self):
        self._exerciseTimeSeconds = 0.0
        self.start_loop()

    @property
    def exerciseTimeSeconds(self) -> float:
        return self._exerciseTimeSeconds

    def start_loop(self):
        async def loop():
            while True:
                await asyncio.sleep(1)
                self.update(1)
        asyncio.create_task(loop())

    def update(self, dt: float):
        self._exerciseTimeSeconds += dt