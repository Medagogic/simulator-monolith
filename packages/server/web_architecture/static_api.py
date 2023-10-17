from __future__ import annotations

from fastapi import APIRouter

class StaticAPI():
    def __init__(self):
        self.router = APIRouter()

class StaticAPIHandler:
    def __init__(self, router: APIRouter):
        self.router = router