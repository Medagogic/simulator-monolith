from typing import Any, Dict
import markdown_to_json
from packages.medagogic_sim.exercise.markdownexercise import MarkdownExercise
from packages.medagogic_sim.exercise.simulation_types import Vitals, abcde_list_to_dict, parse_vital_signs_list, vitals_list_to_dict
from packages.medagogic_sim.history.sim_history import HistoryLog
from packages.medagogic_sim.exercise.simulation4d import NewCurrentStateResponse, LeafyBlossom
from packages.medagogic_sim.gpt import MODEL_GPT4, gpt, UserMessage, SystemMessage, GPTMessage, MODEL_GPT35
import asyncio


from packages.medagogic_sim.logger.logger import get_logger, logging
logger = get_logger(level=logging.INFO)


async def describe_changes(sim: LeafyBlossom, update: str, gpt_model=MODEL_GPT4, cache_skip=False) -> str:
    exercise = sim.exercise

    prompt = f"""
{sim.get_state_markdown(exercise, include_progression=False)}

==================================================

# Instructions
Provide a description of what happens as an immediate consequence of the action presented to you by the user, including any relevant simulation/patient information. Ensure that you aren't thinking too far into the future - this should only be the immediate consequences (as in, within a few seconds) of the update. Write this as definites (ie "will"), not "coulds" or "mights". Keep this as brief as possible while containing all your thoughts and reasoning. It might also be useful to include a mention of parameters which will not change.

Use "Telegraphic Style", where you focus on the most crucial words and omit articles, conjunctions, or other "filler" elements where possible. Telegraphic style: Uses essential words, omits filler, concise, clear. Present tense. Active voice. No articles, conjunctions, or other "filler" elements. For example, "Airway open" instead of "Greta's airway was opened".

Medical accuracy is of utmost importance, as is being sure to include all changes.
    """
    logger.info(f"Calculating consequences for:\n{update}")

    try:
        messages = [SystemMessage(prompt), UserMessage(update)]
        full_response = await gpt(messages, model=gpt_model, max_tokens=1000, temperature=0, cache_skip=cache_skip)
    except Exception as e:
        logger.error(f"Error calculating new immediate state from update: {e}")
        raise e
    
    logger.debug(full_response)

    return full_response + " Other vitals unchanged."



async def implement_changes(sim: LeafyBlossom, update: str, gpt_model=MODEL_GPT4, cache_skip=False) -> str:
    exercise = sim.exercise

    prompt = f"""
{sim.get_state_markdown(exercise, include_progression=False)}

==================================================

# Instructions
Use the instructions from the user to provide updates to the above exercise description. Give only lines which have changed. You should include relevant section headers to make your changes clear.

Importantly, your lines here will be used to overwrite lines in the current state. If any data isn't changing (for example, only part of a line in ABCDE might change), you should carry over the rest of that line (for example, if A changes from "Airway blocked. Loud wheezing" due to wheezing being resolved, you must include the rest of the information in A). If nothing in a line is changed, you should not include that line at all.

Use "Telegraphic Style", where you focus on the most crucial words and omit articles, conjunctions, or other "filler" elements where possible. Telegraphic style: Uses essential words, omits filler, concise, clear. Present tense. Active voice. No articles, conjunctions, or other "filler" elements. For example, "Airway open" instead of "Greta's airway was opened".

Example:
## ABCDE
- A: No free airway. Loud snoring/gurgling sounds.
- B: Intercoastal recession.
...

`Airway open. Snoring/gurgling sounds stop. Other vitals unchanged.`

Response:
## ABCDE
- A: Airway open.
    """
    logger.info(f"Calculating markdown for `{update}`")

    try:
        messages = [SystemMessage(prompt), UserMessage(update)]
        full_response = await gpt(messages, model=gpt_model, max_tokens=1000, temperature=0, cache_skip=cache_skip)
    except Exception as e:
        logger.error(f"Error calculating new immediate state from update: {e}")
        raise e
    
    logger.debug(full_response)

    return full_response.strip()


def validate_change_response(response: str):
    d = markdown_to_json.dictify(response)
    
    if "Current Patient State" in d:
        d = d["Current Patient State"]

    parsed_vitals: Dict[Vitals, Any] = {}
    parsed_abcde: Dict[str, str] = {}

    if "Vital Signs" in d:
        vitals_data = d["Vital Signs"]
        parsed_vitals_timed = vitals_list_to_dict(vitals_data)
        for k, v in parsed_vitals_timed.items():
            parsed_vitals[k] = v.value
    
    if "ABCDE" in d:
        abcde_data = d["ABCDE"]
        parsed_abcde = abcde_list_to_dict(abcde_data)
    
    return parsed_vitals, parsed_abcde


async def validate_and_apply(changes_str: str, exercise: MarkdownExercise) -> None:
    parsed_vitals, parsed_abcde = validate_change_response(changes_str)

    logger.debug(f"Before:\n{exercise.current_state.vital_signs}")
    logger.debug(f"Before:\n{exercise.current_state.abcde.to_markdown()}")

    if parsed_vitals:
        exercise.current_state.vital_signs.update_from_dict(parsed_vitals)
    
    if parsed_abcde:
        exercise.current_state.abcde.update_from_dict(parsed_abcde)

    logger.debug(f"After:\n{exercise.current_state.vital_signs}")
    logger.debug(f"After:\n{exercise.current_state.abcde.to_markdown()}")


async def calculate_new_current_state(sim: LeafyBlossom, update: str, gpt_model=MODEL_GPT4, cache_skip=False) -> str:
    change_description = await describe_changes(sim, update, gpt_model=gpt_model, cache_skip=cache_skip)
    changes_to_implement = await implement_changes(sim, change_description, gpt_model=gpt_model, cache_skip=cache_skip)
    await validate_and_apply(changes_to_implement, sim.exercise)

    return change_description

if __name__ == "__main__":
    logger.level = logging.DEBUG

    async def main():   
        history_log = HistoryLog()
        sim = LeafyBlossom("pediatric_septic_shock", history_log)

        logger.info(sim.get_state_markdown(sim.exercise, include_progression=False))

        change_description = await describe_changes(sim, "Dr Johnson started a Chin Lift", gpt_model=MODEL_GPT4, cache_skip=True)

        changes_to_implement = await implement_changes(sim, change_description, gpt_model=MODEL_GPT4, cache_skip=True)

        logger.info(changes_to_implement)

        await validate_and_apply(changes_to_implement, sim.exercise)


    asyncio.run(main())