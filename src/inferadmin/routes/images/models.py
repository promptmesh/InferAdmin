from pydantic import BaseModel
from datetime import datetime


class DockerImage(BaseModel):
    repo: str
    id: str
    path: str
    tag: str
    created: datetime
    size: float


class GetImagesResponse(BaseModel):
    images: list[DockerImage]


class PostImageRequest(BaseModel):
    repo: str


class DeleteImageRequest(BaseModel):
    id: str