from fastapi import APIRouter
from .models import GetVolumesResponse
from pathlib import Path
from datetime import datetime
import shutil

from .models import Volume

from inferadmin.config.loader import config_manager

router = APIRouter(prefix="/volumes")


@router.get("/")
async def get_volumes() -> GetVolumesResponse:
    volume_path = Path(config_manager.get_config().model_storage_path)
    # Grab total space in GB
    total_space = shutil.disk_usage(volume_path).total / (1024**3)
    # Grab Used space in GB
    used_space = shutil.disk_usage(volume_path).used / (1024**3)
    # Grab Date Created
    date_created = volume_path.stat().st_ctime
    # Convert to datetime
    date_created = datetime.fromtimestamp(date_created)

    volume = Volume(
        name=volume_path.name,
        total_volume_size=total_space,
        volume_size_used=used_space,
        date_created=date_created,
    )
    response = GetVolumesResponse(volumes=[volume])
    return response
