from datetime import datetime
from typing import Any
from pydantic import BaseModel
from inferadmin.routes.standard_models import engines

class LLM(BaseModel):
    id: str
    model_name: str
    engine: engines
    deployment_date: datetime
    status: str

class GetLlmResponse(BaseModel):
    llms: list[LLM]

class PostLlmRequest(BaseModel):
    model_name: str
    engine: engines
    args: dict[str, Any]

class DeleteLlmRequest(BaseModel):
    id: str