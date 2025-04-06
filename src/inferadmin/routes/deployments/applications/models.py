from pydantic import BaseModel
from datetime import datetime
from inferadmin.routes.standard_models import application_types

class Applications(BaseModel):
    id: str
    name: str
    state: str
    type: application_types
    deployed: datetime

class GetApplicationsResponse(BaseModel):
    applications: list[Applications]

class PutApplicationRequest(BaseModel):
    name: str
    type: application_types
    args: dict

class DeleteApplicationRequest(BaseModel):
    id: str