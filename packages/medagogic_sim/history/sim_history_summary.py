from typing import List, Dict, Type, TYPE_CHECKING
import asyncio
from packages.medagogic_sim.gpt.medagogic_gpt import gpt, MODEL_GPT35, UserMessage

if TYPE_CHECKING:
    from packages.medagogic_sim.history.sim_history import ChatMessage, HistoryLog, Event, EventTypes, Intervention, Assessment

class HistoryCondenser:
    @staticmethod
    async def condense_history(history_markdown: str):
        condenser_prompt = f"""
Using the following strategies, please condense the provided history list, ensuring that the most recent events are kept in more detail than the distant ones: summarization, timestamp consolidation, abbreviation, removal of redundant information, and grouping of related events. Keep in mind that the goal is to strike a balance between brevity and clarity while retaining the context and meaning of the original events.
Note that this history is ongoing, not a complete record of events, so you should not assume that the history will end with the last event in the list, ie do not assume actions have finished. If actions are still in progress, report them as ongoing.
Do not invent anything. The facts presented here must remain the same. You may only change the way they are presented.

History List:
{history_markdown}

- An action has not been started unless it is in a [START ACTION] line.
- Do not include any [TAGS] in your response. Your job is to remove those.

Remember to prioritize more recent events for detailed representation while reducing the level of detail for distant events. Your response should be at most 5 sentences, but if there is not much to summarise then you may keep it shorter.
        """.strip()

        response = await gpt([UserMessage(condenser_prompt)], model=MODEL_GPT35, temperature=0)

        response = f"## Summary:\n{response}\n"

        condensed_history = response.strip()

        return condensed_history
    
if __name__ == "__main__":
    async def test_history_condenser():
        from packages.medagogic_sim.history.sim_history import ChatMessage, HistoryLog, Event, EventTypes, Intervention, Assessment

        # Create a HistoryLog and populate it with some events
        history_log = HistoryLog()
        history_log.add_event(ChatMessage(name="Team Lead", content="Hello, world"))
        history_log.add_event(Assessment(npc_name="Dr Johnson", content="Assessed airway, found no obstructions"))
        history_log.add_event(Intervention(npc_name="Dr Johnson", content="Started giving oxygen"))

        # Get a condensed history summary
        summary = await HistoryCondenser.get_summary(history_log, last_n=1)
        print(f"Condensed Summary: {summary}")

    # Run the test
    asyncio.run(test_history_condenser())