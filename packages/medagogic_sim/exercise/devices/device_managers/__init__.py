from .iv_access import IVAccessManager, IVAccessParams
from .io_access import IOAccessManager, IOAccessParams
from .ekg import EKGConnection, EKGConnectionParams
from .nibp import NIBPMonitor, NIBPMonitorParams
from .pulse_oximeter import PulseOximeter, PulseOximeterParams
from .ventilator import Ventilator, VentilatorParams
from .continuous_glucometer import ContinuousGlucometer, ContinuousGlucometerParams


from typing import List
from packages.medagogic_sim.action_db.actions_for_brains import ActionModel

def get_device_action_models() -> List[ActionModel]:
    devices = [
        IVAccessManager,
        IOAccessManager,
        EKGConnection,
        NIBPMonitor,
        PulseOximeter,
        Ventilator,
        ContinuousGlucometer
    ]

    return [device.get_action_model() for device in devices]