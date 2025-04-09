from typing import Literal
from pydantic import BaseModel
from datetime import datetime


class Model(BaseModel):
    repo_id: str
    path: str
    size_gb: float
    last_updated: datetime | None


class GetModelsResponse(BaseModel):
    models: list[Model]


class PostModelRequest(BaseModel):
    repo_id: str
    source: Literal["Huggingface"]