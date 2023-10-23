from prompt_toolkit import print_formatted_text as print
from prompt_toolkit.formatted_text import FormattedText
from pydantic import BaseModel
import rx.core.typing
from rx.subject import Subject

class NPCSpeech(BaseModel):
    npc_id: str
    npc_name: str
    text: str

class IOManager:
    def __init__(self) -> None:
        self.on_npc_speak: rx.core.typing.Subject[NPCSpeech, NPCSpeech] = Subject()

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