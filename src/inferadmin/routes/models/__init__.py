from fastapi import APIRouter
from .models import GetModelsResponse, PostModelRequest, DeleteModelRequest

from .support import scan_hf_models_directory, delete_model, download_hf_model

router = APIRouter(prefix="/models")


@router.get("/list")
async def get_models() -> GetModelsResponse:
    models = await scan_hf_models_directory()
    response = GetModelsResponse(models=models)
    return response


@router.post("/pull")
async def post_models(data: PostModelRequest):
    repo_id = data.repo_id
    source = data.source
    if source == "Huggingface":
        await download_hf_model(repo_id)


@router.post("/delete")
async def delete_models(data: DeleteModelRequest):
    await delete_model(data.repo_id)
