from fastapi import APIRouter
from .models import GetImagesResponse, PutImageRequest, DeleteImageRequest
from inferadmin.routes.standard_models import BasicResponse

router = APIRouter(
    prefix='/images'
)

@router.get('/')
async def get_images() -> GetImagesResponse:
    pass

@router.put('/')
async def put_images(data: PutImageRequest) -> BasicResponse:
    pass

@router.delete('/')
async def delete_images(data: DeleteImageRequest) -> BasicResponse:
    pass