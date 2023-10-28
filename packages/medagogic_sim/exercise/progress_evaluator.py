from enum import Enum
from typing import Dict, Final, List, Optional, Type
import markdown_to_json
from pydantic import BaseModel
from packages.medagogic_sim.context_for_brains import ContextForBrains
from packages.medagogic_sim.exercise.describe_perception import describe_perception, perception_dict_to_markdown
from packages.medagogic_sim.exercise.markdownexercise import MarkdownExercise
from packages.medagogic_sim.history.sim_history import HistoryLog
from packages.medagogic_sim.exercise.simulation4d import NewCurrentStateResponse, LeafyBlossom
from packages.medagogic_sim.gpt import MODEL_GPT4, gpt, UserMessage, SystemMessage, GPTMessage, MODEL_GPT35
import asyncio
import nltk


from packages.medagogic_sim.logger.logger import get_logger, logging
from packages.medagogic_sim.npc_manager import NPCManager
logger = get_logger(level=logging.INFO)


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
    

dummy_checklist = EvaluationChecklist(items=[
    EvaluationChecklistItem(text="Resolve airway obstruction"),
    EvaluationChecklistItem(text="Provide oxygen"),
    EvaluationChecklistItem(text="Check blood glucose"),
])


async def completes_checklist_item(checklist: EvaluationChecklist, gpt_model=MODEL_GPT4, cache_skip=False) -> Optional[int]:
 
    system_content = f"""
You are acting as an evaluator for a virtual simulation training scenario. Determine if the user's action fulfills one of the following checklist items.

{checklist.to_markdown()}

If the user's action fulfills one of the checklist items, respond with "Yes: <id>", eg. "Yes: 8"
If the user's action does not fulfill one of the checklist items, respond with "No"
    """.strip()

    user_content = f"""
Dr. Johnson performed a Chin Lift.
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
        # context = ContextForBrains("pediatric_septic_shock")
        # npc_manager = NPCManager(context)

        completed_item_id = await completes_checklist_item(dummy_checklist, cache_skip=True)

        if completed_item_id is not None:
            logger.info(f"Completed item {completed_item_id}")
            dummy_checklist.set_complete(completed_item_id)

        print(dummy_checklist.to_markdown())


    asyncio.run(main())