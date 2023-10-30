from typing import List, Optional
from pydantic import BaseModel
from packages.medagogic_sim.context_for_brains import ContextForBrains
from packages.medagogic_sim.gpt import MODEL_GPT4, gpt, UserMessage, SystemMessage
from packages.medagogic_sim.history.sim_history import Evt_Assessment, Evt_CompletedIntervention, Evt_StartTask, HistoryEvent
from packages.medagogic_sim.learner_actions.learner_actions import LearnerActions
import asyncio
from rx.subject import Subject


from packages.medagogic_sim.logger.logger import get_logger, logging
logger = get_logger(level=logging.DEBUG)


class EvaluationChecklistItem(BaseModel):
    text: str
    completed: bool = False


class EvaluationChecklist(BaseModel):
    items: List[EvaluationChecklistItem] = []

    def to_markdown(self):
        lines = []
        for i, item in enumerate(self.items):
            lines.append(f"{i+1}. {item.text} {'(Completed!)' if item.completed else ''}")
        return "\n".join(lines)
    
    def set_complete(self, id_from_markdown: int):
        self.items[id_from_markdown-1].completed = True

    def load_learner_actions(path="learner_actions.csv"):
        learner_actions = LearnerActions(path)
        mandatory_items = learner_actions.get_mandatory()
        checklist = EvaluationChecklist(items=[EvaluationChecklistItem(text=action.Action) for action in mandatory_items])
        return checklist


class LearnerActionEvaluator:
    def __init__(self, context: ContextForBrains):
        self.checklist = EvaluationChecklist.load_learner_actions()
        self.context = context
        self.on_learner_action_complete = Subject()

        self.context.history.on_new_event.subscribe(self.handle_new_history_event)


    def handle_new_history_event(self, event: HistoryEvent):
        logger.debug(f"New history event: {event}, type: {type(event)}")
        if isinstance(event, Evt_Assessment):
            asyncio.create_task(self.evaluate_action(event.content))
        elif isinstance(event, Evt_CompletedIntervention):
            asyncio.create_task(self.evaluate_action(event.content))
        elif isinstance(event, Evt_StartTask):
            asyncio.create_task(self.evaluate_action(event.content))


    def get_markdown(self):
        return self.checklist.to_markdown()

    
    async def evaluate_action(self, action: str) -> Optional[EvaluationChecklistItem]:
        logger.info(f"Evaluating action: {action}")

        completed_item_id = await self.completes_checklist_item(action=action, cache_skip=True)

        if completed_item_id is not None:
            logger.info(f"{action} -> {completed_item_id}: {self.checklist.items[completed_item_id-1].text}")
            self.checklist.set_complete(completed_item_id)
            item = self.checklist.items[completed_item_id-1]
            self.on_learner_action_complete.on_next(item)
            return item
        else:
            logger.debug("No item completed")
        
        return None


    async def completes_checklist_item(self, action: str, gpt_model=MODEL_GPT4, cache_skip=False) -> Optional[int]:
        basic_patient_info = self.context.simulation.exercise.basic_info.to_markdown()
        
        system_content = f"""
# Basic Patient Information
{basic_patient_info}

# Checklist
{self.checklist.to_markdown()}

You are acting as an evaluator for a virtual simulation training scenario. Determine if the user's action fulfills one of the above checklist items.
Pay attention to dosages, timing, and other details.
The user's action may only fulfill one of the checklist items.

If the user's action fulfills one of the checklist items, respond with "Yes: <id>", eg. "Yes: 8"
If the user's action does not fulfill one of the checklist items, respond with "No"
    """.strip()

        user_content = f"""
{action}
    """.strip()

        try:
            messages = [SystemMessage(system_content), UserMessage(user_content)]
            full_response = await gpt(messages, model=gpt_model, max_tokens=200, temperature=0, cache_skip=cache_skip)
        except Exception as e:
            logger.error(f"Error calculating new immediate state from update: {e}")
            raise e

        logger.debug(full_response)

        if "Yes" in full_response:
            id = full_response.split(":")[1].strip()
            return int(id)
        else:
            return None


if __name__ == "__main__":
    logger.level = logging.DEBUG

    async def main():
        context = ContextForBrains("pediatric_septic_shock")
        
        evaluator = LearnerActionEvaluator(context)

        # action = "Dr. Johnson performed a Chin Lift."
        action = "Dr. Johnson give bolus (Ringer Acetate 150ml)"

        completed_item = await evaluator.evaluate_action(action)

        print(evaluator.get_markdown())


    asyncio.run(main())