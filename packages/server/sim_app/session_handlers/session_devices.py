from __future__ import annotations
import asyncio
from typing import List, Optional
from pydantic import BaseModel
import socketio
from packages.medagogic_sim.exercise.devices.device_interface import DeviceChangeData
from packages.tools.scribe.src.scribe import scribe_emits
from .med_session_base import MedSessionBase
import packages.medagogic_sim.exercise.devices.device_managers as device_managers

from packages.medagogic_sim.logger.logger import get_logger, logging
logger = get_logger(level=logging.INFO)


class SIO_ConnectedDevices(BaseModel):
    iv_access: List[device_managers.IVAccessParams] = []
    io_access: List[device_managers.IOAccessParams] = []
    ekg_connected: bool
    nibp: Optional[device_managers.NIBPMonitorParams] = None
    pulse_ox: Optional[device_managers.PulseOximeterParams] = None
    ventilator: Optional[device_managers.VentilatorParams] = None
    continuous_glucometer: Optional[device_managers.ContinuousGlucometerParams] = None

class Session_Devices(MedSessionBase):
    def __init__(self, session_id: str, sio: socketio.AsyncServer):
        MedSessionBase.__init__(self, session_id=session_id, sio=sio)
        self.medsim.context.device_interface.on_device_change.subscribe(self.handle_on_device_change)

    def get_state_for_emit(self) -> SIO_ConnectedDevices:
        device_interface = self.medsim.context.device_interface
        device_update = SIO_ConnectedDevices(
            iv_access=list(device_interface.iv_manager.connected_ivs.values()),
            io_access=list(device_interface.io_manager.connected_ios.values()),
            ekg_connected=device_interface.ekg_manager.ekg_connected,
            nibp=device_interface.nibp_manager.nibp_params,
            pulse_ox=device_interface.pulse_ox_manager.connection_params,
            ventilator=device_interface.ventilator_manager.connection_params,
            continuous_glucometer=device_interface.continuous_glucometer_manager.connection_params,
        )
        return device_update

    async def send_full_state(self, sid: str) -> None:
        asyncio.create_task(self.emit_device_update(self.get_state_for_emit(), to=sid))


    def handle_on_device_change(self, data: DeviceChangeData) -> None:
        asyncio.create_task(self.emit_device_update(self.get_state_for_emit()))

    @scribe_emits("device_update", SIO_ConnectedDevices)
    async def emit_device_update(self, device_update: SIO_ConnectedDevices, to=None) -> None:
        await self.emit("device_update", device_update.model_dump(), to=to)