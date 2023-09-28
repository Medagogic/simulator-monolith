import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

class UserHandler:
    def __init__(self, user_id: int):
        self.user_id = user_id

    async def read_item(self, item_id: int):
        return {"user_id": self.user_id, "item_id": item_id}

class UserItemRequest(BaseModel):
    userId: int
    itemId: int

app = FastAPI()

# Dictionary to store UserHandler instances
user_handlers = {1: UserHandler(1), 2: UserHandler(2)}

def get_user_handler(user_item_request: UserItemRequest):
    user_id = user_item_request.userId
    handler = user_handlers.get(user_id)
    if handler is None:
        raise HTTPException(status_code=404, detail="User not found")
    return handler

@app.post("/users/items")
async def read_user_item(
    user_item_request: UserItemRequest,
    user_handler: UserHandler = Depends(get_user_handler)
):
    return await user_handler.read_item(user_item_request.itemId)

if __name__ == "__main__":
    kwargs = {"host": "localhost", "port": 5000, "reload": True}
    uvicorn.run("test2:app", **kwargs)
