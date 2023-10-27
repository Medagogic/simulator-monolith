import markdown_to_json
from packages.medagogic_sim.exercise.markdownexercise import MarkdownExercise
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
    """
    logger.info(f"Calculating new immediate state from update: {update}")

    try:
        messages = [SystemMessage(prompt), UserMessage(update)]
        full_response = await gpt(messages, model=gpt_model, max_tokens=1000, temperature=0, cache_skip=cache_skip)
    except Exception as e:
        logger.error(f"Error calculating new immediate state from update: {e}")
        raise e

    return full_response



async def implement_changes(sim: LeafyBlossom, update: str, gpt_model=MODEL_GPT4, cache_skip=False) -> None:
    exercise = sim.exercise

    prompt = f"""
{sim.get_state_markdown(exercise, include_progression=False)}

==================================================

# Instructions
Use the instructions from the user to provide updates to the above exercise description. Give only lines which have changed. You should include relevant section headers to make your changes clear.

When describing states (eg for ABCDE), write in Telegraph style (ie "Airway open" instead of "Greta's airway was opened").
    """
    logger.info(f"Calculating new immediate state from update: {update}")

    try:
        messages = [SystemMessage(prompt), UserMessage(update)]
        full_response = await gpt(messages, model=gpt_model, max_tokens=1000, temperature=0, cache_skip=cache_skip)
    except Exception as e:
        logger.error(f"Error calculating new immediate state from update: {e}")
        raise e

    return full_response.strip()


def validate_change_response(response: str) -> bool:
    logger.info(response)

    d = markdown_to_json.dictify(response)
    
    for k, v in d.items():
        print(k, v)


if __name__ == "__main__":
    logger.level = logging.DEBUG

    async def main():   
        history_log = HistoryLog()
        sim = LeafyBlossom("pediatric_septic_shock", history_log)

        logger.info(sim.get_state_markdown(sim.exercise, include_progression=False))

        # change_description = await describe_changes(sim, "Dr Johnson started a Chin Lift", gpt_model=MODEL_GPT4, cache_skip=True)

        change_description = """
Greta's airway immediately opens up with the chin lift. The snoring/gurgling sounds  lessen as the free airway is restored, allowing for better ventilation. Her oxygen saturation, however, remains unchanged at 85%.""".strip()
        
        changes_to_implement = await implement_changes(sim, change_description, gpt_model=MODEL_GPT4, cache_skip=False)

        validate_change_response(changes_to_implement)

    asyncio.run(main())