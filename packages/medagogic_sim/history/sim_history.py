import asyncio
from pydantic import BaseModel
from typing import List, Optional, Union, Type
from packages.medagogic_sim.history.sim_history_summary import HistoryCondenser

class Event(BaseModel):
    timestamp: float = None # type: ignore

    def __str__(self):
        return "Generic event"

class ChatMessage(Event):
    name: str
    content: str

    def __str__(self):
        return f"{self.name}: {self.content}"

class Assessment(Event):
    npc_name: str
    content: str

    def __str__(self):
        return f"{self.npc_name}: {self.content}"

class Intervention(Event):
    npc_name: str
    content: str

    def __str__(self):
        return f"{self.npc_name}: {self.content}"

EventTypes = Union[ChatMessage, Assessment, Intervention]

class HistoryLog:
    def __init__(self) -> None:
        self.log: List[EventTypes] = []
        self.condenser = HistoryCondenser()
        self.cached_history: str = "- This is the start of the simulation. Nothing has happened yet, there has been no communication from the team lead, etc."
        self.current_task: Optional[asyncio.Task] = None

    def get_time(self) -> float:
        return 0.0

    def add_event(self, event: EventTypes):
        event.timestamp = self.get_time()
        self.log.append(event)

        if self.current_task and not self.current_task.done():
            self.current_task.cancel()
        self.current_task = asyncio.create_task(self.get_latest_summary())

    def get_filtered_log(self, filter_types: List[Type[Event]] = []) -> List[EventTypes]:
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

    def get_markdown(self, filter_types: List[Type[Event]] = [], last_n: int=0) -> str:
        markdown = ""
        for event in self.get_filtered_log(filter_types)[-last_n:]:
            markdown += f"- {event} @ {self.relative_time_string(event.timestamp)}\n"
        return markdown
    
    async def get_latest_summary(self, filter_types: List[Type[Event]] = [], last_n: int=0) -> str:

        async def get_summary(filter_types: List[Type[Event]] = [], last_n=0) -> str:
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
        history_log.add_event(ChatMessage(name="Alice", content="Hi"))
        history_log.add_event(Assessment(npc_name="npc_1", content="System update"))

        # Get history filtered by multiple types
        print(history_log.get_filtered_log(filter_types=[ChatMessage, Assessment]))

        # Get markdown for specific event types
        print(history_log.get_markdown(filter_types=[ChatMessage, Assessment], last_n=1))

    asyncio.run(main())

