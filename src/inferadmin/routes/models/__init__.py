from fastapi import APIRouter
from .models import GetModelsResponse, PutModelRequest, DeleteModelRequest

from .support import scan_hf_models_directory, delete_model, download_hf_model

router = APIRouter(
    prefix='/models'
)

@router.get('/')
async def get_models() -> GetModelsResponse:
    models = scan_hf_models_directory()
    return {'models': models}

@router.put('/')
async def put_models(data: PutModelRequest):
    repo_id = data.repo_id
    source = data.source
    if source == "Huggingface":
        download_hf_model(repo_id)

@router.delete('/')
async def delete_models(data: DeleteModelRequest):
    repo_id = data.repo_id
    delete_model(repo_id)