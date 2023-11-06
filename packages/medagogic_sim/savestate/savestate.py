import asyncio
from typing import Type
from packages.medagogic_sim.context_for_brains import ContextForBrains
from packages.medagogic_sim.history.sim_history import Evt_Chat_Event, EventTypesByTypeName
from pydantic import TypeAdapter


class SaveStateStorage:
    def __init__(self, context: ContextForBrains):
        self.context = context

        self.context.history.add_event(Evt_Chat_Event(content="Welcome to the Medagogic Simulator!"))

    def save(self):
        current_markdown = self.context.simulation.exercise.to_markdown()
        log = self.context.history.log

        print(current_markdown)

        for event in log:
            print(event.model_dump())


if __name__ == "__main__":
    async def main():
        context = ContextForBrains("pediatric_septic_shock")

        storage = SaveStateStorage(context)

        # storage.save()
        storage.load()

    asyncio.run(main())