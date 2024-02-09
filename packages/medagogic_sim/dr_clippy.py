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
from rx.subject import Subject


from packages.medagogic_sim.logger.logger import get_logger, logging
from packages.medagogic_sim.npcs.npc_manager import NPCManager
logger = get_logger(level=logging.DEBUG)


async def get_suggestions(context: ContextForBrains, npc_manager: NPCManager, gpt_model=MODEL_GPT4, cache_skip=False):
    sim = context.simulation
    exercise = sim.exercise

    npc_summaries: List[str] = []
    for id, npc in npc_manager.npcs.items():
        npc_summaries.append(npc.markdown_summary())
    npc_summary_str = "\n\n".join(npc_summaries)

    connected_device_lines = context.device_interface.full_state_markdown(only_connected=True)
    if len(connected_device_lines) == 0:
        connected_device_lines = ["No devices connected yet."]
    connected_devices_str = "\n".join(connected_device_lines)

    basic_info_str = context.simulation.exercise.basic_info.to_markdown()

    observations_dict = await describe_perception(sim)
    observations_str = perception_dict_to_markdown(observations_dict)

    exposed_vitals = context.get_exposed_vitals()
    exposed_vitals_str = exposed_vitals.to_markdown().strip()
    if len(exposed_vitals_str) == 0:
        exposed_vitals_str = "No vitals monitored."

    difficulty_levels = [
        "The Team Lead is a beginner level student. Give examples of specific instructions which could be given to the team.",
        "The Team Lead is an intermediate level student, be detailed in your help and explanations, including showing some of your reasoning to help them learn.",
        "The Team Lead is an advanced level student, go in-depth with your medical details to help them fully understand the whats, whys, and hows of the protocols.",
    ]

    # full_sim_state = {sim.get_state_markdown(exercise, include_progression=False)}

    sim_state = f"""
# Basic Info
{basic_info_str}

# Observations
{observations_str}

# Monitored Vitals
{exposed_vitals_str}

# Connected Devices/Equipment
{connected_devices_str}

# Relevant Protocols
- ABCDE (Airway, Breathing, Circulation, Disability, Exposure)
    """.strip()

    instructions = f"""
You are acting as an advisor (aka a fancy AI autocomplete) for the team lead in a virtual simulation training scenario.

Your advice should focus on the relevant protocols, and only focus on the most important issues for the next 1-2 mins. Write sentences, not bullet points, ignore the style of the user input when writing your advice. You do not need to cover all the issues, just the 2-3 most critical matters. 

{difficulty_levels[0]}

Your reply must be MAX 3 SENTENCES. Anything more will be ignored. Use "Telegraphic Style", where you focus on the most crucial words and omit articles, conjunctions, or other "filler" elements where possible. Telegraphic style: Uses essential words, omits filler, concise, clear. Present tense. Active voice. No articles, conjunctions, or other "filler" elements. Do not prefix with "Priority one:" or similar.
    """.strip()

    try:
        messages = [SystemMessage(instructions), UserMessage(sim_state)]
        full_response = await gpt(messages, model=gpt_model)
    except Exception as e:
        logger.error(f"Error calculating new immediate state from update: {e}")
        raise e

    logger.debug(full_response)

    # split full_response into sentences
    sentences: List[str] = nltk.sent_tokenize(full_response.strip())
    sentences = [s.strip() for s in sentences if len(s.strip()) > 0]

    return sentences


class DrClippyOutput(BaseModel):
    advice: List[str] = []


class DrClippy:
    def __init__(self, context: ContextForBrains, npc_manager: NPCManager):
        self.context = context
        self.npc_manager = npc_manager
        self.context.simulation.on_state_change.subscribe(self.handle_sim_state_change)
        self.cached_output: Optional[DrClippyOutput] = None
        self.update_advice_task = asyncio.create_task(self.__recalculate_advice())
        self.on_new_advice = Subject()


    def handle_sim_state_change(self, new_exercise: MarkdownExercise):
        self.update_advice_task = asyncio.create_task(self.__recalculate_advice())

    async def recalculate_advice(self):
        if self.update_advice_task is None:
            self.update_advice_task = self.__recalculate_advice()

        await self.update_advice_task

    async def __recalculate_advice(self):
        logger.debug("Recalculating advice...")
        advice_sentences = await get_suggestions(self.context, self.npc_manager, cache_skip=False)
        self.cached_output = DrClippyOutput(advice=advice_sentences)
        self.on_new_advice.on_next(self.cached_output)

    
    @property
    def latest_advice(self):
        return self.cached_output


if __name__ == "__main__":
    logger.level = logging.DEBUG

    async def main():
        context = ContextForBrains("pediatric_septic_shock")
        npc_manager = NPCManager(context)

        dr_clippy = DrClippy(context, npc_manager)

        await dr_clippy.update_advice_task

        logger.info(dr_clippy.cached_output)


        # advice_sentences = await get_suggestions(context, npc_manager, cache_skip=True)

        # for sentence in advice_sentences:
        #     logger.info(sentence)

    asyncio.run(main())