from aiodocker import DockerError
from fastapi import APIRouter

from inferadmin.docker import DockerManager
from inferadmin.routes.standard_models import BasicResponse

from .models import DeleteImageRequest, GetImagesResponse, PostImageRequest

router = APIRouter(prefix="/images")


@router.get("/")
async def get_images() -> GetImagesResponse:
    pass


@router.post("/")
async def post_images(data: PostImageRequest) -> BasicResponse:
    """Pull a docker image"""
    docker = DockerManager.get()

    try:
        await docker.images.pull(data.repo)
    except Exception as e:
        return BasicResponse(success=False, error_message=str(e))

    return BasicResponse(success=True, error_message=None)


@router.delete("/")
async def delete_images(data: DeleteImageRequest) -> BasicResponse:
    """Delete a docker image"""
    docker = DockerManager.get()

    try:
        await docker.images.get(data.id)
    except DockerError as e:
        if e.status == 404:
            return BasicResponse(success=True, error_message=None)

    try:
        await docker.images.delete(data.id)
    except Exception as e:
        return BasicResponse(success=False, error_message=str(e))

    return BasicResponse(success=True, error_message=None)
