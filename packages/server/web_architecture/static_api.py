from __future__ import annotations

from fastapi import APIRouter
from web_architecture.webhandler import WebHandler_Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from web_architecture.sessionhandler import SessionHandler_Base

class StaticAPI():
    def __init__(self):
        self.router = APIRouter()

class StaticAPIHandler:
    def __init__(self, router: APIRouter):
        self.router = router