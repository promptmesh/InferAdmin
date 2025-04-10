from fastapi import APIRouter, HTTPException
from loguru import logger

from .models import GetImagesResponse, PostImageRequest, DockerImage, DeleteImageRequest
from .support import pull_container_image, get_container_images, remove_container_image

from datetime import datetime

router = APIRouter(prefix="/images")

# Label to identify images managed by InferAdmin
INFERADMIN_LABEL = "managed-by-inferadmin"


@router.get("/list")
async def get_images() -> GetImagesResponse:
    """Get all docker images managed by InferAdmin"""
    try:
        # Get InferAdmin managed images using the support function
        managed_images = get_container_images()

        images_list = []

        for image in managed_images:
            # Use the first tag that contains "-inferadmin" for this image
            inferadmin_tag = next(
                (tag for tag in image.tags if "-inferadmin" in tag), None
            )

            if not inferadmin_tag:
                continue  # Skip if no valid tag

            # Extract base info from the tag
            image_id = image.id.replace("sha256:", "")[:12]
            # Original image name is before the "-inferadmin" part
            original_tag = inferadmin_tag.split("-inferadmin")[0]

            repo_parts = original_tag.split(":")
            repo = repo_parts[0]
            tag_value = repo_parts[1] if len(repo_parts) > 1 else "latest"
            path = repo
            created = image.attrs.get("Created", datetime.now())
            # Convert size to GB (size is in bytes)
            size = image.attrs.get("Size", 0) / (1024 * 1024 * 1024)

            docker_image = DockerImage(
                repo=repo,
                id=image_id,
                path=path,
                tag=tag_value,
                created=created,
                size=round(size, 2),
            )

            images_list.append(docker_image)

    except Exception as e:
        logger.error(f"fetching images: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching images: {str(e)}")

    return GetImagesResponse(images=images_list)


@router.post("/pull")
async def post_images(data: PostImageRequest):
    """Pull a docker image and mark it as managed by InferAdmin"""
    try:
        # Use the support function to pull and tag the image
        image = await pull_container_image(data.repo)

        # Create response using format expected by API
        return {
            "status": "success",
            "message": f"Image {data.repo} pulled and tagged as {image.tags[0]}",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to pull image: {str(e)}")


@router.delete("/delete")
async def delete_images(data: DeleteImageRequest):
    """Delete a docker image"""
    try:
        # Use the support function to remove the image
        await remove_container_image(data.id)
        return {"status": "success", "message": f"Image {data.id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete image: {str(e)}")
