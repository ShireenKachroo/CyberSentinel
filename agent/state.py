# maintain state across multi step tool interactions

from __future__ import annotations
from typing import Annotated, TypedDict, List, Dict, Any
from langchain_core.messages import BaseMessage
import operator

class InvestigationState(TypedDict):
    event_id: str
    target_ip: str | None
    messages: Annotated[List[BaseMessage], operator.add]
    investigation_steps: List[Dict[str, Any]]
    retrieved_evidence: Dict[str, Any]
    investigation_complete: bool
    final_report: Dict[str, Any] | None