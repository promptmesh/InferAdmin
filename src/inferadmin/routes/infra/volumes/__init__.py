from fastapi import APIRouter
from .models import GetVolumesResponse

router = APIRouter(
    prefix='/volumes'
)

@router.get('/')
async def get_volumes() -> GetVolumesResponse:
    pass