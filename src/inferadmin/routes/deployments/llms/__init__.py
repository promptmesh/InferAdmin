from fastapi import APIRouter
from .models import GetLlmResponse, PostLlmRequest, DeleteLlmRequest
from inferadmin.routes.standard_models import BasicResponse

router = APIRouter(
    prefix='/llms'
)

@router.get('/')
async def get_llms() -> GetLlmResponse:
    pass

@router.post('/')
async def post_llms(data: PostLlmRequest) -> BasicResponse:
    pass

@router.delete('/')
async def delete_llms(data: DeleteLlmRequest) -> BasicResponse:
    pass