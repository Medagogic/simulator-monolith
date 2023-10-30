import asyncio
from pydantic import BaseModel
from typing import List, Optional, Tuple, Union, Type
from packages.medagogic_sim.history.sim_history_summary import HistoryCondenser
from packages.medagogic_sim.logger.logger import get_logger, logging
from rx.subject import Subject


logger = get_logger(level=logging.INFO)


class HistoryEvent(BaseModel):
    timestamp: float = None # type: ignore

    def __str__(self):
        return "Generic event"
    

class Evt_Chat_Base(HistoryEvent):
    content: str
    type: str


class Evt_Chat_NPCMessage(Evt_Chat_Base):
    npc_id: str
    type: str = "npc_message"

    def __str__(self):
        return f"{self.npc_id}: {self.content}"

class Evt_Chat_Event(Evt_Chat_Base):
    npc_id: Optional[str] = None
    type: str = "event"

    def __str__(self):
        return f"{self.content}"

class Evt_Chat_HumanMessage(Evt_Chat_Base):
    target_npc_id: Optional[str] = None
    type: str = "human_message"

    def __str__(self):
        return f"Team Lead: {self.content}"


class Evt_Assessment(HistoryEvent):
    npc_name: str
    content: str

    def __str__(self):
        return f"{self.npc_name}: {self.content}"

class Evt_StartTask(HistoryEvent):
    npc_name: str
    content: str

    def __str__(self):
        return f"{self.npc_name}: {self.content}"
    
class Evt_TaskConsequence(HistoryEvent):
    npc_name: str
    content: str

    def __str__(self):
        return f"{self.npc_name}: {self.content}"

class Evt_CompletedIntervention(HistoryEvent):
    npc_name: str
    content: str

    def __str__(self):
        return f"{self.npc_name}: {self.content}"

EventTypes = Union[Evt_Chat_Base, Evt_Assessment, Evt_CompletedIntervention, Evt_StartTask, Evt_TaskConsequence]

class HistoryLog:
    def __init__(self) -> None:
        self.log: List[EventTypes] = []
        self.condenser = HistoryCondenser()
        self.cached_history: str = "- This is the start of the simulation. Nothing has happened yet, there has been no communication from the team lead, etc."
        self.current_task: Optional[asyncio.Task] = None

        self.on_new_event: Subject = Subject()

    def get_time(self) -> float:
        return 0.0

    def add_event(self, event: EventTypes):
        event.timestamp = self.get_time()
        self.log.append(event)

        for m in self.log[-10:]:
            logger.debug(f"LOG: {str(m)}")

        if self.current_task and not self.current_task.done():
            self.current_task.cancel()
        self.current_task = asyncio.create_task(self.get_latest_summary())

        self.on_new_event.on_next(event)

    def get_filtered_log(self, filter_types: List[Type[HistoryEvent]] = []) -> List[EventTypes]:
        if filter_types:
            return [event for event in self.log[:] if any(isinstance(event, t) for t in filter_types)]
        return self.log

    def relative_time_string(self, event_time: float) -> str:
        current_time_seconds = self.get_time()
        relative_time = abs(current_time_seconds - event_time)
        minutes = relative_time // 60
        seconds = relative_time % 60
        if minutes > 0:
            return f"{minutes} minutes {seconds} seconds ago"
        else:
            return f"{seconds} seconds ago"

    def get_markdown(self, filter_types: List[Type[HistoryEvent]] = [], last_n: int=0) -> str:
        markdown = ""
        for event in self.get_filtered_log(filter_types)[-last_n:]:
            markdown += f"- {event} @ {self.relative_time_string(event.timestamp)}\n"
        return markdown
    
    async def get_latest_summary(self, filter_types: List[Type[HistoryEvent]] = [], last_n: int=0) -> str:

        async def get_summary(filter_types: List[Type[HistoryEvent]] = [], last_n=0) -> str:
            if len(self.get_filtered_log(filter_types=filter_types)) == 0:
                return "- This is the start of the simulation. Nothing has happened yet, there has been no communication from the team lead, etc."
            return await HistoryCondenser.condense_history(self.get_markdown(filter_types=filter_types, last_n=last_n))
        
        self.cached_history = await get_summary(filter_types=filter_types, last_n=last_n)
        return self.cached_history
    
    def get_cached_summary(self) -> str:
        return self.cached_history
    

    

if __name__ == "__main__":
    async def main():
        history_log = HistoryLog()
        history_log.add_event(Evt_Chat_HumanMessage(content="Hi"))
        history_log.add_event(Evt_Assessment(npc_name="npc_1", content="Some assessment"))

        # Get history filtered by multiple types
        print(history_log.get_filtered_log(filter_types=[Evt_Chat_Base, Evt_Assessment]))

        # Get markdown for specific event types
        print(history_log.get_markdown(filter_types=[Evt_Chat_Base, Evt_Assessment], last_n=5))

    asyncio.run(main())

