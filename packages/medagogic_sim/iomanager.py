from __future__ import annotations
from typing import TYPE_CHECKING, Optional

from prompt_toolkit import print_formatted_text as print
from prompt_toolkit.formatted_text import FormattedText
from pydantic import BaseModel
import rx.core.typing
from rx.subject import Subject

if TYPE_CHECKING:
    from packages.medagogic_sim.actions_for_brains import TaskCall

class NPCSpeech(BaseModel):
    npc_id: str
    npc_name: str
    text: str

class NPCAction(BaseModel):
    npc_id: str
    npc_name: str
    task_info: str

class NPCThinking(BaseModel):
    npc_id: str
    npc_name: str
    about: Optional[str] = None

class IOManager:
    def __init__(self) -> None:
        self.on_npc_speak: rx.core.typing.Subject[NPCSpeech, NPCSpeech] = Subject()
        self.on_npc_start_action: rx.core.typing.Subject[NPCAction, NPCAction] = Subject()
        self.on_npc_finished_action: rx.core.typing.Subject[NPCAction, NPCAction] = Subject()
        self.on_npc_thinking_updated: rx.core.typing.Subject[NPCThinking, NPCThinking] = Subject()

    def npc_start_thinking(self, npc_id: str, npc_name: str, about: str):
        print(FormattedText([
            ('#008888', f"{npc_name} is thinking about '{about}'..."),
        ]))
        self.on_npc_thinking_updated.on_next(NPCThinking(npc_id=npc_id, npc_name=npc_name, about=about))

    def npc_stop_thinking(self, npc_id: str, npc_name: str):
        self.on_npc_thinking_updated.on_next(NPCThinking(npc_id=npc_id, npc_name=npc_name, about=None))

    def npc_speak(self, npc_id: str, npc_name: str, text: str):
        print(FormattedText([
            ('#42eff5 bold', f"{npc_name}: "),
            ('#ffffff', text),
        ]))
        self.on_npc_speak.on_next(NPCSpeech(npc_id=npc_id, npc_name=npc_name, text=text))
    
    def simulation_alert(self, text: str):
        print(FormattedText([
            ('#ffaa00 bold', f"SIM ALERT: "),
            ('#ffaa00', text),
        ]))

    def npc_start_action(self, npc_id: str, npc_name: str, task: TaskCall):
        task_info = f"Start: {task.call_data.name}"
        if len(task.call_data.params) > 0:
            task_info += f": {', '.join(task.call_data.params)}"
        print(FormattedText([
            ('#ffbb00 bold', f"Action - {npc_name}: "),
            ('#ffffff', task_info),
        ]))
        self.on_npc_start_action.on_next(NPCAction(npc_id=npc_id, npc_name=npc_name, task_info=task_info))

    def npc_finished_action(self, npc_id: str, npc_name: str, task: TaskCall):
        task_info = f"Finished: {task.call_data.name}"
        if len(task.call_data.params) > 0:
            task_info += f": {', '.join(task.call_data.params)}"
        print(FormattedText([
            ('#ffbb00 bold', f"Action finished - {npc_name}: "),
            ('#ffffff', task_info),
        ]))
        self.on_npc_finished_action.on_next(NPCAction(npc_id=npc_id, npc_name=npc_name, task_info=task_info))