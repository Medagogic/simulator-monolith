from packages.medagogic_sim.context_for_brains import ContextForBrains
from packages.medagogic_sim.dialog_router import TeamLeadDialog
from packages.medagogic_sim.npc import logger as npc_logger
import logging
import asyncio

from packages.medagogic_sim.npc_manager import NPCManager

if __name__ == "__main__":
    npc_logger.setLevel(logging.DEBUG)

    async def main():
        context = ContextForBrains()
        npc_manager = NPCManager(context)

        input_dialog = TeamLeadDialog("check the airway and perform a chin lift if needed")
        await npc_manager.process_dialog(input_dialog)

        while True:
            await asyncio.sleep(1)

    asyncio.run(main())