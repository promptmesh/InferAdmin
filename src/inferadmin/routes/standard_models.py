from pydantic import BaseModel
from typing import Literal, TypeAlias

engines: TypeAlias = Literal['vLLM']
application_types: TypeAlias = Literal['OpenWebUI']


class BasicResponse(BaseModel):
    success: bool
    error_message: str | None