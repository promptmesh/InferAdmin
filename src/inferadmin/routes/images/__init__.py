from aiodocker import DockerError
from fastapi import APIRouter, HTTPException

from inferadmin.docker import DockerManager

from .models import DeleteImageRequest, GetImagesResponse, PostImageRequest, DockerImage

from datetime import datetime
import json

router = APIRouter(prefix="/images")

# Label to identify images managed by InferAdmin
INFERADMIN_LABEL = "managed-by-inferadmin"


@router.get("/")
async def get_images() -> GetImagesResponse:
    """Get all docker images managed by InferAdmin"""
    docker = DockerManager.get()
    
    images_list = []
    
    try:
        # List all images with filter for our label
        all_images = await docker.images.list()
        
        for image in all_images:
            print(f"Processing image: {image}") # TODO clean prints after format of labeled images is known
            # Check if the image has our management label
            labels = image.get('Labels', {})
            print(f"Labels: {labels}")

            if labels and INFERADMIN_LABEL in labels.keys():
                repo_tags = image.get('RepoTags', [])

                if not repo_tags:
                    continue  # Skip images with no tags
                
                # Use the first tag for display
                tag = repo_tags[0]
                
                image_id = image.get('Id', '').replace('sha256:', '')[:12]
                repo_parts = tag.split(':')
                repo = repo_parts[0]
                tag_value = repo_parts[1] if len(repo_parts) > 1 else 'latest'
                path = repo
                created = datetime.fromtimestamp(image.get('Created', 0))
                size = image.get('Size', 0) / (1024 * 1024 * 1024)  # Convert to GB
                
                docker_image = DockerImage(
                    repo=repo,
                    id=image_id,
                    path=path,
                    tag=tag_value,
                    created=created,
                    size=size
                )
                
                images_list.append(docker_image)
    
    except Exception as e:
        # Log the error but return empty list
        print(f"Error fetching images: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching images: {str(e)}")

    return GetImagesResponse(images=images_list)


@router.post("/")
async def post_images(data: PostImageRequest):
    """Pull a docker image and mark it as managed by InferAdmin"""
    docker = DockerManager.get()

    try:
    #Parse the image reference
        
        repo_parts = data.repo.split(':')
        repo_name = repo_parts[0]
        tag = repo_parts[1] if len(repo_parts) > 1 else 'latest'
        
        # Pull the requested image
        pull_data = await docker.images.pull(data.repo)
        print(f"Pull data: {pull_data}")
        
        # Get the image ID from the pull response
        image_id = None
        if isinstance(pull_data, list):
            for item in pull_data:
                if 'id' in item:
                    image_id = item['id']
                    break
        elif isinstance(pull_data, dict) and 'Id' in pull_data:
            image_id = pull_data['Id']
        
        if not image_id:
            # Try to get the image by its tag
            try:
                image = await docker.images.get(data.repo)
                image_id = image['Id']
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to get image ID after pull: {str(e)}")
        
        # Create a new tag for the InferAdmin managed version
        managed_tag = f"{repo_name}-inferadmin:{tag}"
        
        # Tag the image with our management specific tag
        await docker.images.tag(name=data.repo, repo=managed_tag.split(':')[0], tag=managed_tag.split(':')[1])
        
        # Add our label to the image (note: this actually requires building a new image)
        # We'll skip this for now and rely on the special tag pattern
        
        return {"status": "success", "message": f"Image {data.repo} pulled and tagged as {managed_tag}"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to pull image: {str(e)}")


@router.delete("/")
async def delete_images(data: DeleteImageRequest):
    """Delete a docker image"""
    docker = DockerManager.get()

    try:
        await docker.images.get(data.id)
    except DockerError as e:
        if e.status == 404:
            raise HTTPException(status_code=404, detail="Image not found")
        else:
            raise HTTPException(status_code=500, detail=str(e))
            
    try:
        await docker.images.delete(data.id)
        return {"status": "success", "message": f"Image {data.id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete image: {str(e)}")