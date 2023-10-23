from abc import ABC, abstractmethod
from rx.subject import Subject

class AnimationResolver_Base(ABC):
    def __init__(self) -> None:
        self.on_action_finished: Subject = Subject()

    # @abstractmethod
    # def play_animation(self, agent_id: str, animation_id: str):
    #     pass

    @abstractmethod
    async def resolve_animation(self, agent_id: str, animation_id: str):
        pass