from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Type, TYPE_CHECKING
from pydantic import BaseModel
import asyncio

if TYPE_CHECKING:
    from packages.medagogic_sim.exercise.devices.device_managers.base_handler import DeviceHandler_Base
    from packages.medagogic_sim.exercise.simulation_types import Vitals

from packages.medagogic_sim.actions_for_brains import ActionDatabase, ActionExample
from packages.medagogic_sim.exercise.devices.device_managers import *

from packages.medagogic_sim.logger.logger import get_logger, logging
logger = get_logger(level=logging.DEBUG)

import rx.core.typing
from rx.subject import Subject


@dataclass
class DeviceChangeData:
    manager: DeviceHandler_Base


class DeviceInterface:
    def __init__(self) -> None:
        self.iv_manager = IVAccessManager()
        self.io_manager = IOAccessManager()
        self.ekg_manager = EKGConnection()
        self.nibp_manager = NIBPMonitor()
        self.pulse_ox_manager = PulseOximeter()
        self.ventilator_manager = Ventilator()
        self.continuous_glucometer_manager = ContinuousGlucometer()

        self.all_managers: List[DeviceHandler_Base] = [
            self.iv_manager,
            self.io_manager,
            self.ekg_manager,
            self.nibp_manager,
            self.pulse_ox_manager,
            self.ventilator_manager,
            self.continuous_glucometer_manager,
        ]

        self.on_device_change: rx.core.typing.Subject[DeviceChangeData, DeviceChangeData] = Subject()

    def full_state_markdown(self, only_connected=False) -> List[str]:
        states: List[str] = []
        for manager in self.all_managers:
            if manager.is_connected or not only_connected:
                states.append(manager.get_state())
        
        return states
    
    def get_manager_from_call_data(self, call_data: ActionDatabase.CallData) -> DeviceHandler_Base | None:
        for manager in self.all_managers:
            if call_data.name.lower() in manager.action_name.lower():
                return manager
        return None
    
    def handle_call(self, call_data: ActionDatabase.CallData) -> str:
        manager = self.get_manager_from_call_data(call_data)
        if manager is None:
            raise Exception(f"Could not find manager for {call_data.name}")
        response = manager.handle_call(call_data)
        self.on_device_change.on_next(DeviceChangeData(manager=manager))
        return response

    def exposed_vitals(self) -> List[Vitals]:
        vitals: List[Vitals] = []
        for manager in self.all_managers:
            vitals.extend(manager.exposed_vitals())
        return list(set(vitals))


if __name__ == "__main__":
    async def main():
        device_interface = DeviceInterface()

        action_db = ActionDatabase()

        input_commands = [
            "get IV access",
            "get IO access",
            "connect the EKG",
            "connect the BP monitor",
            "connect the pulse oximeter",
            # "connect the ventilator",
            # "connect the continuous glucometer",
        ]

        for input_command in input_commands:
            action = action_db.get_relevant_actions(input_command)[0]
            example = action.examples[0]
            if isinstance(example, ActionExample):
                task_call = action_db.get_action_from_call(action.examples[0].action, action.examples[0].input)
            else:
                task_call = action_db.get_action_from_call(action.name, example)

            logger.info(task_call.full_input)

            response = device_interface.handle_call(task_call.call_data)
            logger.info(response)

            logger.info(device_interface.full_state_markdown(only_connected=True))
            logger.info(device_interface.exposed_vitals())

    asyncio.run(main())