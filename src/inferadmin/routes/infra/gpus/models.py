from pydantic import BaseModel

class GpuState(BaseModel):
    id: str
    total_vram: float
    used_vram: float
    utilization: float
    power_consumption: float

class GetGpusResponse(BaseModel):
    gpus: list[GpuState]