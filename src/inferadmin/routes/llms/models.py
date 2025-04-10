from pydantic import BaseModel
from datetime import datetime
from typing import Any, Dict, List, Optional
from inferadmin.routes.standard_models import engines


class LLM(BaseModel):
    id: str
    model_name: str
    engine: engines
    image_id: str
    deployment_date: datetime
    status: str


class GetLlmsResponse(BaseModel):
    llms: list[LLM]


class CompletionRequest(BaseModel):
    model_id: str
    prompt: str
    max_tokens: int = 100
    temperature: float = 0.7
    top_p: float = 1.0
    stop: Optional[List[str]] = None


class CompletionResponse(BaseModel):
    id: str
    model_id: str
    text: str
    created: datetime
    usage: Dict[str, int]


class ModelIdRequest(BaseModel):
    model_id: str