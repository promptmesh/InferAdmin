from fastapi import APIRouter
from .models import GetLlmResponse, PutLlmRequest, DeleteLlmRequest
from inferadmin.routes.standard_models import BasicResponse

router = APIRouter(
    prefix='/llms'
)

@router.get('/')
async def get_llms() -> GetLlmResponse:
    pass

@router.put('/')
async def put_llms(data: PutLlmRequest) -> BasicResponse:
    pass

@router.delete('/')
async def delete_llms(data: DeleteLlmRequest) -> BasicResponse:
    pass