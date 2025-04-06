from fastapi import APIRouter
from .models import GetApplicationsResponse, PutApplicationRequest, DeleteApplicationRequest
from inferadmin.routes.standard_models import BasicResponse

router = APIRouter(
    prefix='/applications'
)

@router.get('/')
async def get_applications() -> GetApplicationsResponse:
    pass

@router.put('/')
async def put_applications(data: PutApplicationRequest) -> BasicResponse:
    pass

@router.delete('/')
async def delete_applications(data: DeleteApplicationRequest) -> BasicResponse:
    pass