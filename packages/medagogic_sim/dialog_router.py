from __future__ import annotations
from typing import TYPE_CHECKING, Final, Optional, Tuple

from pydantic import BaseModel
if TYPE_CHECKING:
    from packages.medagogic_sim.context_for_brains import ContextForBrains
    from packages.medagogic_sim.npc_manager import NPCManager

from typing import List
from packages.medagogic_sim.gpt.medagogic_gpt import MODEL_GPT4, gpt_streamed_lines, UserMessage, SystemMessage, GPTMessage
import asyncio
from packages.medagogic_sim.condense_npcs import getNPCSummary
from rx.subject import Subject

from packages.medagogic_sim.dialog_router_prompt import prompt as rules_for_response

import logging
from packages.medagogic_sim.logger.logger import get_logger
logger = get_logger(name="router", level=logging.DEBUG)


class Dialog(BaseModel):
    from_id: str
    content: str
    to_id: Optional[str] = None

def TeamLeadDialog(content: str) -> Dialog:
    return Dialog(from_id=TEAM_LEAD_ID, content=content)

TEAM_LEAD_ID: Final = "Team Lead"

class DialogRouter():
    def __init__(self, context: ContextForBrains, npc_manager: NPCManager) -> None:
        self.context = context
        self.npc_manager = npc_manager
        self.model = MODEL_GPT4
        logger.info(f"{self.__class__.__name__} initialized using {self.model}")
        self.on_new_routing = Subject()


    async def route_input(self, input_dialog: Dialog):
        if input_dialog.from_id not in self.npc_manager.npcs:
            if input_dialog.from_id != TEAM_LEAD_ID:
                raise Exception(f"Unknown from_id: {input_dialog.from_id}")
            else:
                speaker_name = "Team Lead"
        else:
            speaker_name = self.npc_manager.npcs[input_dialog.from_id].definition.name

        logger.info(f"Processing routing for Dialog ({speaker_name}): {input_dialog.content}")
        system_prompt = await self.get_instruction_prompt()

        user_prompt = f"""
INPUT:
{speaker_name}: "{input_dialog.content}"
""".strip()

        messages: List[GPTMessage] = [
            SystemMessage(system_prompt),
            UserMessage(user_prompt)
        ]

        temperature = 0

        routed_dialogs: List[Dialog] = []

        async for line in gpt_streamed_lines(messages, model=self.model+"-0613", max_tokens=200, temperature=temperature):
            if not line.startswith("//"):
                routed_dialog = self.parse_routed_dialog(input_dialog, line) 
                if routed_dialog:
                    yield routed_dialog
                    routed_dialogs.append(routed_dialog)

        if not routed_dialogs:
            logger.error(f"No routed dialogs found for input: {input_dialog}")


    def parse_routed_dialog(self, input_dialog: Dialog, response: str) -> Dialog | None:
        parsed = self.get_dialog_from_line(response)
        if parsed:
            to_id, content = parsed
            return Dialog(from_id=input_dialog.from_id, content=content, to_id=to_id)

        return None


    def get_dialog_from_line(self, full_line: str) -> Tuple[str, str] | None:
        if not full_line.find(" <- "):
            return None

        try:
            recipient_name, text = full_line.split(" <- ")
            to_npc = self.npc_manager.find_npc_by_name(recipient_name)
            if to_npc:
                return to_npc.id, text
        except Exception as e:
            logger.error(f"Error parsing {full_line}: {e}")
        
        return None


    async def get_instruction_prompt(self) -> str:
        history_summary = self.context.history.get_cached_summary()

        vignette = self.context.metadata.vignette
        patient_history = self.context.simulation.exercise.patient_background

        return f"""
# INSTRUCTIONS:
{rules_for_response}

# SIMULATION STATE:
{vignette}

{patient_history}

# History
{history_summary}

# NPCs
{getNPCSummary(self.npc_manager, skip_busy=True)}

# INSTRUCTIONS:
- Your input is from a noisy speech-to-text system, so it may contain errors, background chatter, or other irrelevant information.
- You should try to filter (or fix) the incoming text, so that it makes sense contextually. Some of the text may be irrelevant.
- Then, split up the filtered input into invididual commands, and route the commands to the most suitable NPC to respond to it.
- Each command should only be routed to one NPC. Don't duplicate commands.
- Each command must be routed to exactly one NPC. Don't drop commands.
- Base your routings on the current state of the simulation, the recent history (to allow for back-and-forth conversation), the current state of the NPCs, and their expertise.

    """.strip()
        

if __name__ == "__main__":
    from packages.medagogic_sim.context_for_brains import ContextForBrains
    from packages.medagogic_sim.npc_manager import NPCManager
    logger.setLevel(logging.DEBUG)
    async def main():
        context = ContextForBrains()
        npc_manager = NPCManager(context)
        router = DialogRouter(context, npc_manager)

        inputs = [
            Dialog(from_id=TEAM_LEAD_ID, content="what do you think team, what are we dealing with here ?"),
        ]

        for sapling_dialog in inputs:
            async for routed_dialog in router.route_input(sapling_dialog):
                print(routed_dialog)


    asyncio.run(main())