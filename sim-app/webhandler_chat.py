from __future__ import annotations
from web_architecture.webhandler import WebHandler_Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from web_architecture.sessionhandler import SimulationSessionHandler


class ChatWebHandler(WebHandler_Base):
    def __init__(self, sesh_handler: SimulationSessionHandler):
        WebHandler_Base.__init__(self, namespace="chat", sesh_handler=sesh_handler)

        self.router.get("/test-get")(self.handle_test)


    async def handle_test(self):
        return {"content": f"Hello world in {self.session_id}"}


    async def on_message(self, sid, msg):
        print(f"on_message {msg} in {self.namespace}")
        await self.emit("response", {"content": f"{msg} @ {self.namespace}"})  # or send to everyone
