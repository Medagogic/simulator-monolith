from prompt_toolkit import print_formatted_text as print
from prompt_toolkit.formatted_text import FormattedText

class IOManager:
    def __init__(self):
        pass

    def npc_speak(self, npc_id: str, npc_name: str, text: str):
        print(FormattedText([
            ('#42eff5 bold', f"{npc_name}: "),
            ('#ffffff', text),
        ]))
    
    def simulation_alert(self, text: str):
        print(FormattedText([
            ('#ffaa00 bold', f"SIM ALERT: "),
            ('#ffaa00', text),
        ]))