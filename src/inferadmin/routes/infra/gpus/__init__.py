import shutil
import subprocess
from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from .models import GetGpusResponse, GpuState

router = APIRouter(prefix="/gpus")


@router.get("/")
async def get_gpus() -> GetGpusResponse:
    """Get GPU information"""

    nvidia_smi = shutil.which("nvidia-smi")
    if nvidia_smi is None:
        raise HTTPException(status_code=500, detail="nvidia-smi not found")

    gpus: list[GpuState] = []

    try:
        output = subprocess.check_output(
            [
                nvidia_smi,
                "--query-gpu=uuid,utilization.gpu,power.draw,memory.total,memory.used",
                "--format=csv,noheader,nounits",
            ],
            encoding="utf-8",
        )
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"nvidia-smi failed: {e.output}")

    for line in output.splitlines():
        if not line or line.startswith("#"):
            continue

        try:
            uuid, utilization, power, total, used = line.split(",")
            gpus.append(
                GpuState(
                    uuid=uuid,
                    total_vram=float(total),
                    used_vram=float(used),
                    utilization=float(utilization),
                    power_consumption=float(power),
                )
            )
        except (ValidationError, ValueError):
            continue

    return GetGpusResponse(gpus=gpus)
