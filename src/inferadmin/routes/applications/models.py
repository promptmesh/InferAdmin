from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any
from inferadmin.routes.standard_models import application_types


class Application(BaseModel):
    id: str
    name: str
    state: str
    type: application_types
    deployed: datetime
    host_port: int
    gpu_uuids: Optional[list[str]] = None
    logs: Optional[str] = None


class GetApplicationsResponse(BaseModel):
    applications: list[Application]


class PostApplicationRequest(BaseModel):
    name: str
    app_type: application_types
    image_id: str
    host_port: int = Field(..., description="Port to expose on the host")
    environment: Optional[Dict[str, Any]] = None
    gpu_uuids: Optional[list[str]] = None


class GetApplicationLogsResponse(BaseModel):
    id: str
    logs: str


class DeleteApplicationRequest(BaseModel):
    id: str


class ApplicationIdRequest(BaseModel):
    id: str