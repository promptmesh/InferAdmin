from pydantic import BaseModel


class GpuState(BaseModel):
    uuid: str
    total_vram: float
    used_vram: float
    utilization: float
    power_consumption: float


class GetGpusResponse(BaseModel):
    gpus: list[GpuState]
