# from datetime import datetime
# from enum import Enum
# import json
# from typing import List
# import os

# from pydantic import BaseModel


# class HistoryElementType(Enum):
#     USER_INPUT = "USER INPUT"
#     DIALOG = "DIALOG"
#     START_ACTION = "START ACTION"
#     ACTION_COMPLETE = "ACTION COMPLETE"
    

# class HistoryElement(BaseModel):
#     time: int
#     type: HistoryElementType
#     actor: str
#     text: str

#     def describe(self) -> str:
#         return f"[{self.type.value}] {self.actor}: {self.text}"



# class EventHistory(List[HistoryElement]):
#     def __init__(self, session_name=None, *args, **kwargs):
#         if session_name is None:
#             session_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#         self.session_name = session_name
#         super(EventHistory, self).__init__(*args, **kwargs)

#     def _save(self) -> None:
#         if not os.path.exists("autosim/logs"):
#             os.makedirs("autosim/logs")
#         with open(f"autosim/logs/{self.session_name}.json", "w") as f:
#             items: List[HistoryElement] = self
#             dumpable = [{"time": e.time, "type": e.type.value, "actor": e.actor, "text": e.text} for e in items]
#             json.dump(dumpable, f, indent=4)

#     def append(self, item: HistoryElement):
#         super(EventHistory, self).append(item)
#         self._save()

#     def __add__(self, other):
#         if isinstance(other, list):
#             new_history = EventHistory(self.session_name, super().__add__(other))
#             new_history._save()
#             return new_history
#         else:
#             raise TypeError("unsupported operand type(s) for +: 'AutoSimHistory' and '{}'".format(type(other).__name__))

#     def __setitem__(self, key, value: HistoryElement):  # type: ignore
#         super(EventHistory, self).__setitem__(key, value)
#         self._save()

#     def __delitem__(self, key):
#         super(EventHistory, self).__delitem__(key)
#         self._save()

#     def insert(self, index, item: HistoryElement):
#         super(EventHistory, self).insert(index, item)
#         self._save()


# if __name__ == "__main__":

#     history = EventHistory()
    
#     # 2. Test appending a GPTMessage
#     msg1 = HistoryElement(time=0, type=HistoryElementType.DIALOG, actor="system", text="Test message.")
#     history.append(msg1)

#     # 3. Test adding a GPTMessage
#     msg2 = HistoryElement(time=2, type=HistoryElementType.START_ACTION, actor="Dr Johnson", text="Test message 2.")
#     history = history + [msg2]

#     print(history)