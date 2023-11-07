from __future__ import annotations
from typing import Dict, List, TYPE_CHECKING
import asyncio

if TYPE_CHECKING:
    from packages.medagogic_sim.npcs.npc_manager import NPCManager


def getNPCSummary(npc_manager: NPCManager, skip_id=None, skip_busy=False) -> str:
    lines = []

    for id, npc in npc_manager.npcs.items():
        if id == skip_id:
            continue
        if skip_busy and npc.actioner.current_task_description:
            continue

        lines.append(npc.markdown_summary())

    return "\n".join(lines)


if __name__ == "__main__":
    from packages.medagogic_sim.context_for_brains import ContextForBrains
    from packages.medagogic_sim.npcs.npc_manager import NPCManager
    async def main():
        context = ContextForBrains()
        npc_manager = NPCManager(context)
        print(getNPCSummary(npc_manager))

    asyncio.run(main())