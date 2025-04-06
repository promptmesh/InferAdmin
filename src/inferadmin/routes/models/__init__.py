from fastapi import APIRouter
from .models import GetModelsResponse, PutModelRequest, DeleteModelRequest, PutModelResponse
from inferadmin.routes.standard_models import BasicResponse

router = APIRouter(
    prefix='/models'
)

@router.get('/')
async def get_models() -> GetModelsResponse:
    pass

@router.put('/')
async def put_models(data: PutModelRequest) -> PutModelResponse:
    pass

@router.delete('/')
async def delete_models(data: DeleteModelRequest) -> BasicResponse:
    pass