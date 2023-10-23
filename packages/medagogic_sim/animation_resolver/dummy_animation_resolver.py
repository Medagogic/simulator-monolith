import asyncio
import random
from packages.medagogic_sim.animation_resolver.animation_resolver_base import AnimationResolver_Base


class DummyAnimationResolver(AnimationResolver_Base):
    def __init__(self, min_time=10, max_time=20):
        super().__init__()
        self.min_time = min_time
        self.max_time = max_time


    async def resolve_animation(self, agent_id: str, animation_id: str):
        await asyncio.sleep(self.min_time + (random.random() * (self.max_time - self.min_time)))
        print(f"DummyAnimationResolver: Finished animation {animation_id} for {agent_id}")
        self.on_action_finished.on_next((agent_id, animation_id))
