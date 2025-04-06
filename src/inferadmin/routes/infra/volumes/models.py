from pydantic import BaseModel
from datetime import datetime

class Volume(BaseModel):
    name: str
    total_volume_size: float
    volume_size_used: float
    date_created: datetime

class GetVolumesResponse(BaseModel):
    volumes: list[Volume]