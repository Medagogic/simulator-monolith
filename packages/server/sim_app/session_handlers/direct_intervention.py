from __future__ import annotations
from packages.tools.scribe import scribe_handler
from .med_session_base import MedSessionBase

from packages.medagogic_sim.logger.logger import get_logger, logging
logger = get_logger(level=logging.INFO)



class DirectInterventionSession(MedSessionBase):
    @scribe_handler
    async def on_direct_intervention(self, sid, function_call: str) -> None:
        print(f"Client {sid} called on_direct_intervention `{function_call}` in {self.session_id}")
        task = self.medsim.context.action_db.get_action_from_call(function_call, function_call)
        if task.type == "intervention":
            params_str = ", ".join(task.call_data.params)
            receipt = self.medsim.context.simulation.applyUpdate(f"Dr Whoopie performed action: `{task.call_data.name} ({params_str})`")

            receipt.on_new_immediate_state_generated.subscribe(self.direct_intervention_current_state_recalculated)
            receipt.on_finished.subscribe(self.direct_intervention_finished)
        else:
            raise Exception(f"Task {task} is not an intervention")
    
    def direct_intervention_current_state_recalculated(self, data):
        exercise, comments = data
        logger.info(f"Current state recalculated: {exercise}")
        logger.info(f"Comments: {comments}")

    def direct_intervention_finished(self, null):
        exercise = self.medsim.context.simulation.exercise
        logger.info(f"Finished direct intervention: {exercise}")