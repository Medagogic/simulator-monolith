from dataclasses import dataclass
from typing import List


@dataclass
class TimedEvent:
    time_seconds: float
    event: str

    @property
    def time_string(self) -> str:
        minutes = self.time_seconds // 60
        seconds = self.time_seconds % 60
        if minutes > 0:
            return f"{minutes} minutes {seconds} seconds"
        else:
            return f"{seconds} seconds"
        
    def relative_time_string(self, current_time_seconds: float) -> str:
        relative_time = abs(current_time_seconds - self.time_seconds)

        minutes = relative_time // 60
        seconds = relative_time % 60
        if minutes > 0:
            return f"{minutes} minutes {seconds} seconds ago"
        else:
            return f"{seconds} seconds ago"
        
    def to_markdown(self, current_time_seconds: float) -> str:
        return f"{self.event} @ {self.relative_time_string(current_time_seconds)}"


class InterventionTracker:
    def __init__(self) -> None:
        self.events: List[TimedEvent] = []

    def recordEvent(self, time_seconds: float, event: str):
        self.events.append(TimedEvent(time_seconds, event))

    def to_markdown(self, current_time_seconds: float) -> str:
        markdown = ""
        for event in self.events:
            markdown += f"- {event.to_markdown(current_time_seconds)}\n"
        return markdown