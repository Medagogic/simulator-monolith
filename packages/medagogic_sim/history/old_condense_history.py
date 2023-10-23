# from __future__ import annotations

# from packages.medagogic_sim.history.old_auto_sim_history import EventHistory, HistoryElement, HistoryElementType
# from typing import Dict, List
# from packages.medagogic_sim.gpt.medagogic_gpt import gpt, MODEL_GPT35, UserMessage

# import asyncio

# __cached_condensed_history: Dict[str, str] = {}

# class HistoryTracker:
#     def __init__(self) -> None:
#         self.event_history = EventHistory()

#         self.__update_task = None
#         self.history_summary = "- This is the start of the simulation. Nothing has happened yet, there has been no communication from the team lead, etc."

#     @property   
#     def latest_summary(self) -> str:
#         full_summary = self.history_summary

#         recent_history = "\n".join([h.describe() for h in self.event_history[-10:]])
#         if len(recent_history.strip()) > 0:
#             full_summary += f"""

# ## Recent history (newest at bottom):
# {recent_history}
# """

#         action_history: str = ""
#         for history_event in self.event_history:
#             if history_event.type == HistoryElementType.ACTION_COMPLETE:
#                 action_history += f"- {history_event.describe()}\n"
#         if action_history:
#             full_summary += f"""
# ## Actions taken:
# {action_history}
# """

#         # print(f"================\nGenerated history summary:\n{full_summary}\n====================\n")

#         return full_summary

#     def trigger_update(self):
#         if self.__update_task:
#             self.__update_task.cancel()
#         self.__update_task = asyncio.create_task(self.__update_history())
        
#     async def __update_history(self):
#         self.history_summary = await condense_history(self.event_history)

#     def is_updating(self) -> bool:
#         if self.__update_task:
#             return not self.__update_task.done()
#         return False




# async def condense_history(history_lines: List[HistoryElement]):
#     history_str = ""
#     for element in history_lines[-10:]:
#         if element.type == HistoryElementType.DIALOG:
#             history_str += f"{element.actor}: {element.text})\n"
#         elif element.type == HistoryElementType.START_ACTION:
#             history_str += f"{element.actor}: Start task: {element.text}\n"

#     condenser_prompt = f"""
# Using the following strategies, please condense the provided history list, ensuring that the most recent events are kept in more detail than the distant ones: summarization, timestamp consolidation, abbreviation, removal of redundant information, and grouping of related events. Keep in mind that the goal is to strike a balance between brevity and clarity while retaining the context and meaning of the original events.
# Note that this history is ongoing, not a complete record of events, so you should not assume that the history will end with the last event in the list, ie do not assume actions have finished. If actions are still in progress, report them as ongoing.
# Do not invent anything. The facts presented here must remain the same. You may only change the way they are presented.

# History List:
# {history_str}

# - An action has not been started unless it is in a [START ACTION] line.
# - Do not include any [TAGS] in your response. Your job is to remove those.

# Remember to prioritize more recent events for detailed representation while reducing the level of detail for distant events. Your response should be at most 5 sentences, but if there is not much to summarise then you may keep it shorter.
#     """

#     if condenser_prompt in __cached_condensed_history:
#         return __cached_condensed_history[condenser_prompt]

#     response = await gpt([UserMessage(condenser_prompt)], model=MODEL_GPT35, temperature=0)

#     response = f"## Summary:\n{response}\n"

#     condensed_history = response.strip()
#     __cached_condensed_history[condenser_prompt] = condensed_history

#     return condensed_history

# if __name__ == "__main__":
#     import asyncio
#     import json

#     def format_seconds_to_hhmmss(total_seconds):
#         hours, remainder = divmod(total_seconds, 3600)
#         minutes, seconds = divmod(remainder, 60)
#         return f'{hours:02d}:{minutes:02d}:{seconds:02d}'

#     def load_log(log_path):
#         with open(log_path) as f:
#             data = json.load(f)

#         out_lines = []

#         for entry in data:
#             time = format_seconds_to_hhmmss(entry[0])
#             task = entry[1]
#             actor = entry[2]
#             text = entry[3]

#             out_lines.append(f"{time} {task}: {actor}: {text}")

#         return out_lines


#     async def __main():
#         history_lines = load_log("autosim/logs/2023-04-13_21-19-00.json")
#         print(history_lines)
#         response = await condense_history(history_lines)
#         print(response)

#     asyncio.run(__main())