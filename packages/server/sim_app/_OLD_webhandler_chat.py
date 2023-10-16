# from __future__ import annotations
# from web_architecture.webhandler import WebHandler_Base
# from typing import TYPE_CHECKING, Any, Dict

# if TYPE_CHECKING:
#     from web_architecture.sessionhandler import SessionHandler_Base


# class ChatWebHandler(WebHandler_Base):
#     def __init__(self, sesh_handler: SessionHandler_Base):
#         WebHandler_Base.__init__(self, namespace="chat", sesh_handler=sesh_handler)

#         self.router.get("/test-get")(self.handle_test)


#     async def handle_test(self):
#         return {"content": f"Hello world in {self.session_id}"}
    

#     async def on_connect(self, sid, environ):
#         print(f"on_connect {sid} in {self.namespace}")
#         await self.emit("response", {"content": f"Hello to {sid}!"})


#     async def on_message(self, sid, data: Dict[str, Any]):
#         print(f"on_message {data} in {self.namespace}")
#         await self.emit("response", {"content": f"{data} @ {self.namespace}"})  # or send to everyone


# if __name__ == "__main__":
#     def main():
#         doc = ChatWebHandler.generate_doc()
#         print(doc)

#     main()