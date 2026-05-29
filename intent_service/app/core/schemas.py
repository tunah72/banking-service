from __future__ import annotations
from pydantic import BaseModel


class IntentResult(BaseModel):
    intent: str
    confidence: float
    reason: str = ""
    top_k: list[dict] = []
