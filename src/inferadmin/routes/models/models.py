from typing import Literal
from pydantic import BaseModel
from datetime import datetime
from inferadmin.routes.standard_models import BasicResponse

class Model(BaseModel):
    name: str
    id: str
    is_local: bool
    last_updated: datetime | None

class GetModelsResponse(BaseModel):
    models: list[Model]

class PutModelRequest(BaseModel):
    name: str
    source: Literal["Huggingface"]

class PutModelResponse(BasicResponse):
    streaming: bool

class DeleteModelRequest(BaseModel):
    name: str