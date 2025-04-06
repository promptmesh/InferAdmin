from fastapi import APIRouter
from inferadmin.routes.infra.gpus import router as gpus_router
from inferadmin.routes.infra.volumes import router as volumes_router

router = APIRouter(
    prefix='/infra'
)

router.include_router(gpus_router)
router.include_router(volumes_router)

@router.get('/')
async def get_volumes():
    pass
