from fastapi import APIRouter
# from inferadmin.routes.deployments.llms import router as llms_router
from inferadmin.routes.deployments.applications import router as applications_router

router = APIRouter(
    prefix='/deployments'
)

#router.include_router(llms_router) # commenting because I think we only need a single deployment router
router.include_router(applications_router)