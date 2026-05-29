from __future__ import annotations
from typing import Literal
from pydantic import BaseModel


class HistoryMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class CustomerRequest(BaseModel):
    message: str
    history: list[HistoryMessage] = []


class IntentResult(BaseModel):
    intent: str
    confidence: float
    reason: str = ""
    top_k: list[dict] = []


class PriorityResult(BaseModel):
    level: Literal["low", "medium", "high"]
    reason: str
    matched_keywords: list[str]


class PolicyResult(BaseModel):
    intent: str
    policy_text: str
    guidelines: list[str]


class DraftResult(BaseModel):
    draft_reply: str
    missing_info: list[str]
    next_action: str


class ValidationResult(BaseModel):
    is_valid: bool
    issues: list[str]
    should_escalate: bool


class RoutingResult(BaseModel):
    action: Literal["reply", "ask_more", "escalate"]
    final_response: str
    reason: str


class WorkflowTrace(BaseModel):
    intent: IntentResult
    priority: PriorityResult
    policy: PolicyResult
    draft: DraftResult
    validation: ValidationResult
    routing: RoutingResult


class AgentResponse(BaseModel):
    message: str
    action: str
    trace: WorkflowTrace
