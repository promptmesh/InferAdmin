from fastapi import APIRouter
from inferadmin.routes.applications import router as applications_router
from inferadmin.routes.llms import router as llms_router
from inferadmin.routes.images import router as images_router
from inferadmin.routes.infra import router as infra_router
from inferadmin.routes.models import router as models_router

from inferadmin.openapi_tags import Tag

router = APIRouter(prefix="/api/v1")

router.include_router(applications_router, tags=[Tag.applications])
router.include_router(llms_router, tags=[Tag.llms])
router.include_router(images_router, tags=[Tag.images])
router.include_router(infra_router, tags=[Tag.infra])
router.include_router(models_router, tags=[Tag.models])
