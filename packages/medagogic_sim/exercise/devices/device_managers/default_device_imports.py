from __future__ import annotations
from typing import TYPE_CHECKING, List, Dict, Optional

from enum import Enum
from pydantic import BaseModel, Field
from packages.medagogic_sim.exercise.devices.device_utils import FuzzyEnumMatcher
from packages.medagogic_sim.exercise.devices.device_managers.base_handler import DeviceHandler_Base
from packages.medagogic_sim.action_db.actions_for_brains import ActionDatabase
from packages.medagogic_sim.exercise.simulation_types import Vitals
from packages.medagogic_sim.action_db.actions_for_brains import ActionExample, ActionModel
import re

from packages.medagogic_sim.logger.logger import get_logger, logging
