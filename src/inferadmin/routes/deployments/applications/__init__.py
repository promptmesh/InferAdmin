from fastapi import APIRouter
from .models import GetApplicationsResponse, PostApplicationRequest, DeleteApplicationRequest


router = APIRouter(
    prefix='/applications'
)

@router.get('/')
async def get_applications() -> GetApplicationsResponse:
    pass

@router.post('/')
async def post_applications(data: PostApplicationRequest):
    pass

@router.delete('/')
async def delete_applications(data: DeleteApplicationRequest):
    pass