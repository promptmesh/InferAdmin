from fastapi import APIRouter
from inferadmin.routes.deployments import router as deployment_router
from inferadmin.routes.images import router as images_router
from inferadmin.routes.infra import router as infra_router
from inferadmin.routes.models import router as models_router

router = APIRouter(
    prefix='/api/v1'
)

router.include_router(deployment_router)
router.include_router(images_router)
router.include_router(infra_router)
router.include_router(models_router)