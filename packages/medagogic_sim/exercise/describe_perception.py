from enum import Enum
from typing import Dict, Final, Optional, Type
import markdown_to_json
from pydantic import BaseModel
from packages.medagogic_sim.exercise.markdownexercise import MarkdownExercise
from packages.medagogic_sim.history.sim_history import HistoryLog
from packages.medagogic_sim.exercise.simulation4d import NewCurrentStateResponse, LeafyBlossom
from packages.medagogic_sim.gpt import MODEL_GPT4, gpt, UserMessage, SystemMessage, GPTMessage, MODEL_GPT35
import asyncio


from packages.medagogic_sim.logger.logger import get_logger, logging
logger = get_logger(level=logging.INFO)


class PerceptionKey(str, Enum):
    BREATHING_SOUNDS = "Breathing sounds"
    VOCALIZATIONS = "Vocalizations"
    CONSCIOUSNESS = "Consciousness"
    CHEST_MOVEMENTS = "Chest movements"
    SKIN = "Skin"
    WOUNDS_BLEEDING = "Wounds/bleeding"

PerceptionDict = Dict[PerceptionKey, str]

def perception_dict_to_markdown(perceptions: PerceptionDict) -> str:
    return "\n".join([f" - {key.value}: {value}" for key, value in perceptions.items()])


async def describe_perception(sim: LeafyBlossom, gpt_model=MODEL_GPT4, cache_skip=False) -> PerceptionDict:
    exercise = sim.exercise

    sim_state = f"""
{sim.get_state_markdown(exercise, include_progression=False)}
    """

    perception_keys = "\n".join([f" - {key.value}" for key in PerceptionKey])

    perception_examples_dict: PerceptionDict = {
        PerceptionKey.BREATHING_SOUNDS: "Snoring, strained breathing",
        PerceptionKey.VOCALIZATIONS: "Crying",
        PerceptionKey.CHEST_MOVEMENTS: "Rapid breathing, chest retractions",
        PerceptionKey.SKIN: "Pale, slightly mottled, sweaty",
        PerceptionKey.WOUNDS_BLEEDING: "Bleeding from head wound"
    }
    perception_examples = perception_dict_to_markdown(perception_examples_dict)

    instructions = f"""
You are acting as the eyes and ears for the team lead in a virtual simulation training scenario.

Given your provided simulation information, describe what the team lead would percieve from the patient. Include sight and audio. Write in Telegraph style (ie "Airway open" instead of "Greta's airway was opened", or "Snoring" instead of "There is snoring").

Only include things directly related to the patient. Be brief. Only include things which would be easily or passively observed, not things which would require active investigation.

Provide your response as a markdown list of keys/values, The keys may be:
{perception_keys}

Example:
{perception_examples}

Important: If the value for some key would be nothing or empty, either skip that key, or provide a value of None.
    """.strip()

    try:
        messages = [SystemMessage(instructions), UserMessage(sim_state)]
        full_response = await gpt(messages, model=gpt_model, max_tokens=1000, temperature=0, cache_skip=cache_skip)
    except Exception as e:
        logger.error(f"Error calculating new immediate state from update: {e}")
        raise e

    logger.debug(full_response)

    return parse_perception_response(full_response)


def parse_perception_response(full_response: str) -> PerceptionDict:
    lines = full_response.strip().split("\n")

    perceptions: PerceptionDict = {}

    for line in lines:
        raw_key, raw_value = line.split(":", 1)
        key = raw_key.replace("-", "").strip()

        value: Optional[str] = raw_value.strip()
        if not value:
            value = None
        elif value.lower() == "none":
            value = None

        logger.debug(f"key: {key}, value: {value}")

        if value is None:
            continue

        try:
            key_enum = PerceptionKey(key)
        except:
            logger.error(f"Invalid PerceptionKey `{key}` while parsing `{line}`")
            continue

        perceptions[key_enum] = value.strip()

    logger.debug(perceptions)

    return perceptions
    



if __name__ == "__main__":
    logger.level = logging.DEBUG

    async def main():   
        history_log = HistoryLog()
        sim = LeafyBlossom("pediatric_septic_shock", history_log)

        logger.info(sim.get_state_markdown(sim.exercise, include_progression=False))

        perception_dict = await describe_perception(sim, gpt_model=MODEL_GPT4, cache_skip=True)

        import json
        print(json.dumps(perception_dict, indent=4))

        print(perception_dict_to_markdown(perception_dict))


    asyncio.run(main())