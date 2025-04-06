from fastapi import APIRouter
from .models import GetGpusResponse
router = APIRouter(
    prefix='/gpus'
)

@router.get('/')
async def get_gpus() -> GetGpusResponse:
    pass