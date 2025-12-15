from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class RunCreate(BaseModel):
    prompt: str
    pipeline: str = "lite"
    mode: str = "live"


class RunSummary(BaseModel):
    run_id: str
    created_at: str
    status: str
    pipeline: str
    mode: str
    topic_prompt: str


class RunDetail(RunSummary):
    models: List[str]
    chairman_model: str
    anonymization_map: Dict[str, str]
    stages: List[Dict[str, Any]]
    final: Dict[str, Any]
