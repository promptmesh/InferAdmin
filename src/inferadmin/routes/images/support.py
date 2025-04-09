import docker
from fastapi import HTTPException, status

from inferadmin.docker import DockerManager

INFERADMIN_LABEL = "managed-by-inferadmin"


def pull_container_image(image_name: str):
    """
    Pull a Docker image from the Docker registry and mark it as managed by InferAdmin.
    """
    try:
        # Pull the image
        print(f"Pulling image: {image_name}")
        image = DockerManager.client.images.pull(image_name)

        # Tag the image to identify it as managed by InferAdmin
        tag_name = f"{image_name}-inferadmin"
        image.tag(tag_name)

        print(f"Image {image_name} pulled and tagged successfully.")
        return image
    except docker.errors.APIError as e:
        print(f"Error pulling image: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to pull Docker image: {str(e)}",
        )


def get_image_name_by_id(image_id: str):
    """
    Get the image name by its ID.

    Args:
        image_id: The ID of the image to retrieve.

    Returns:
        The name of the image.
    """
    try:
        image = DockerManager.client.images.get(image_id)
        # check if the image is managed by InferAdmin
        if not any("-inferadmin" in tag for tag in image.tags):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Image with ID {image_id} is not managed by InferAdmin.",
            )
        return image.tags[0] if image.tags else None
    except docker.errors.ImageNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Image with ID {image_id} not found.",
        )
    except docker.errors.APIError as e:
        print(f"Error fetching image: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching Docker image: {str(e)}",
        )
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error while fetching image: {str(e)}",
        )


def get_container_images():
    """
    Get a list of all Docker images managed by InferAdmin.
    """
    try:
        images = DockerManager.client.images.list()
        inferadmin_images = [
            image for image in images if any("-inferadmin" in tag for tag in image.tags)
        ]
        return inferadmin_images
    except docker.errors.APIError as e:
        print(f"Error fetching images: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching Docker images: {str(e)}",
        )
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error while fetching images: {str(e)}",
        )


def remove_container_image(image_id: str):
    """
    Remove a Docker image from the local system only if it is managed by InferAdmin.

    Args:
        image_id: The ID or name of the image to remove
    """
    try:
        # First check if this is a direct image ID
        try:
            image = DockerManager.client.images.get(image_id)
            # Check if any tag for this image contains -inferadmin
            if any("-inferadmin" in tag for tag in image.tags):
                DockerManager.client.images.remove(image.id, force=True)
                print(f"Image with ID {image_id} removed successfully.")
                return
        except docker.errors.ImageNotFound:
            # Not a direct ID, try to find by name/tag
            pass

        # Then check if it's a tag name
        images = DockerManager.client.images.list()
        for image in images:
            # Check if this image is managed by InferAdmin
            inferadmin_tag = next(
                (tag for tag in image.tags if "-inferadmin" in tag), None
            )
            if not inferadmin_tag:
                continue

            # Check if requested image_id matches any tag or the original image name
            original_tag = inferadmin_tag.split("-inferadmin")[0]
            if image_id == original_tag or image_id in image.tags:
                DockerManager.client.images.remove(image.id, force=True)
                print(f"Image {image_id} removed successfully.")
                return

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Image {image_id} not found or not managed by InferAdmin.",
        )
    except docker.errors.APIError as e:
        print(f"Error removing image: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error removing Docker image: {str(e)}",
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error while removing image: {str(e)}",
        )
