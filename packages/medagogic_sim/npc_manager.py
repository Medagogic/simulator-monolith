from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from packages.medagogic_sim.context_for_brains import ContextForBrains

from typing import Dict
import asyncio
from packages.medagogic_sim.npc import MedicalNPC
from packages.medagogic_sim.npc_definitions import NPC_DEFINITIONS
from packages.medagogic_sim.dialog_router import TEAM_LEAD_ID, Dialog, DialogRouter

import logging
from packages.medagogic_sim.logger.logger import get_logger
logger = get_logger(level=logging.DEBUG)


class NPCManager:
    def __init__(self, context: ContextForBrains):
        self.npcs: Dict[str, MedicalNPC] = {}
        self.router = DialogRouter(context, self)

        npc_definitions = NPC_DEFINITIONS
        for i, definition in enumerate(npc_definitions):
            npc_id = f"npc_{i}"
            self.npcs[npc_id] = MedicalNPC(context=context, definition=definition, id=npc_id)


    async def process_dialog(self, dialog: Dialog):
        if dialog.to_id:
            npc = self.npcs[dialog.to_id]
            await npc.process_input(dialog.content)
        else:
            tasks = []
            async for routed_dialog in self.router.route_input(dialog):
                task = asyncio.create_task(self.process_dialog(routed_dialog))
                tasks.append(task)
            while len(tasks) > 0:
                done, pending = await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
                tasks = list(pending)
    

    def find_npc_by_name(self, npc_name: str) -> MedicalNPC | None:
        def x(s: str):
            return s.lower().replace(" ", "").replace(".", "")
        for npc_id, npc in self.npcs.items():
            if x(npc.definition.name) == x(npc_name):
                return npc
        return None
    



if __name__ == "__main__":
    from packages.medagogic_sim.context_for_brains import ContextForBrains
    logger.level = logging.INFO
    async def main():
        context = ContextForBrains()
        npc_manager = NPCManager(context)

        npc_inputs = [
            # Sapling_Routed_Dialog("Nurse Taylor", Sapling_Dialog("Team Lead", "Can you connect the monitors?")),
            # Sapling_Routed_Dialog("Nurse Smith", Sapling_Dialog("Team Lead", "Nurse Smith please start on IV access")),
            Dialog(from_id=TEAM_LEAD_ID, content="Let's check airway patency and start getting IV access"),
            # Dialog(from_id=TEAM_LEAD_ID, content="Actually stop getting IV access, let's do IO access instead", to_id="npc_2"),
            # Sapling_Routed_Dialog("Nurse Smith", Sapling_Dialog("Team Lead", "Okay actually cancel the epinephrine, we will decide later.")),
        ]

        for npc_input in npc_inputs:
            await npc_manager.process_dialog(npc_input)

    asyncio.run(main())