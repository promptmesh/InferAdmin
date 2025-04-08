import docker
import os
from pathlib import Path
from typing import List
from fastapi import HTTPException
from datetime import datetime

from inferadmin.docker import DockerManager
from inferadmin.config.loader import config_manager
from inferadmin.state.manager import StateManager
from inferadmin.state import STATE_DIR
from inferadmin.routes.deployments.llms.models import LLM
from inferadmin.routes.images.support import get_container_images

# Create state manager for LLM deployments
llm_manager = StateManager(STATE_DIR, "llms.json", LLM)

def deploy_llm(model_name: str, engine: str, image_id: str, host_port: int, 
               gpu_ids: List[int], tensor_parallel: int, max_model_len: int) -> LLM:
    """Deploy a LLM inference engine with explicit parameters."""
    try:
        # Verify the image exists and is managed by InferAdmin
        if not is_managed_image(image_id):
            raise HTTPException(status_code=400, 
                               detail=f"Image {image_id} is not managed by InferAdmin")
        
        # Generate a unique ID for this deployment
        from uuid import uuid4
        deployment_id = str(uuid4())[:8]
        
        # Get the correct image name/tag
        image = get_image_name(image_id)
        
        # Check if the model exists
        model_storage_path = config_manager.get_config().model_storage_path
        model_folder_name = model_name.replace('/', '_')
        model_path = os.path.join(model_storage_path, model_folder_name)
        
        if not Path(model_path).exists():
            raise HTTPException(status_code=404, detail=f"Model not found: {model_name}")
        
        # Configure container based on engine type
        if engine == "vLLM":
            container = deploy_vllm(
                image=image, 
                model_path=model_path,
                deployment_id=deployment_id,
                host_port=host_port,
                gpu_ids=gpu_ids,
                tensor_parallel=tensor_parallel,
                max_model_len=max_model_len
            )
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported engine: {engine}")
        
        # Create LLM record
        llm = LLM(
            id=deployment_id,
            model_name=model_name,
            engine=engine,
            image_id=image_id,
            deployment_date=datetime.now(),
            status="starting",
            container_id=container.id,
            host_port=host_port,
            gpu_ids=gpu_ids
        )
        
        # Save to state
        llm_manager.add(llm)
        
        return llm
        
    except HTTPException:
        raise
    except docker.errors.ImageNotFound:
        raise HTTPException(status_code=404, detail=f"Image not found: {image_id}")
    except docker.errors.APIError as e:
        raise HTTPException(status_code=500, detail=f"Docker API error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to deploy LLM: {str(e)}")

def deploy_vllm(image: str, model_path: str, deployment_id: str, host_port: int,
                gpu_ids: List[int], tensor_parallel: int, max_model_len: int):
    """Deploy a vLLM container with specific configuration."""
    # Set up container configuration
    ports = {f'8000/tcp': ('0.0.0.0', host_port)}
    volumes = {model_path: {'bind': '/models', 'mode': 'ro'}}
    
    # Build vLLM command
    gpu_arg = ','.join(str(gpu) for gpu in gpu_ids) if gpu_ids else 'all'
    
    command = [
        "python", "-m", "vllm.entrypoints.api_server",
        "--model", "/models",
        "--tensor-parallel-size", str(tensor_parallel),
        "--max-model-len", str(max_model_len),
        "--host", "0.0.0.0",
        "--port", "8000"
    ]
    
    # Add GPU args if specific GPUs requested
    if gpu_ids:
        command.extend(["--gpu-ids", gpu_arg])
    
    # Create device requests for GPU access
    device_requests = [docker.types.DeviceRequest(count=-1, capabilities=[['gpu']])]
    
    # Launch container
    container = DockerManager.client.containers.run(
        image,
        command=command,
        detach=True,
        ports=ports,
        volumes=volumes,
        name=f"inferadmin-llm-{deployment_id}",
        labels={
            "managed-by": "inferadmin",
            "deployment-type": "llm",
            "deployment-id": deployment_id
        },
        device_requests=device_requests
    )
    
    return container

def is_managed_image(image_id: str) -> bool:
    """Check if an image is managed by InferAdmin."""
    managed_images = get_container_images()
    
    # Check if image_id matches any of the managed images
    for image in managed_images:
        if image.id.startswith(image_id) or any(image_id in tag for tag in image.tags):
            return True
    
    return False

def get_image_name(image_id: str) -> str:
    """Get the full image name from an ID or partial name."""
    managed_images = get_container_images()
    
    for image in managed_images:
        # Check if the image ID matches
        if image.id.startswith(image_id):
            # Return the first inferadmin tag if available
            return next((tag for tag in image.tags if "-inferadmin" in tag), image.tags[0])
        
        # Check if any tag matches
        for tag in image.tags:
            if image_id in tag:
                return tag
    
    # If not found, return the original ID
    return image_id

def get_all_llms() -> List[LLM]:
    """Get all LLM deployments with current status."""
    llms = llm_manager.get_all()
    
    # Update status for each LLM
    for llm in llms:
        if hasattr(llm, 'container_id') and llm.container_id:
            llm.status = get_container_status(llm.container_id)
    
    return llms

def get_container_status(container_id: str) -> str:
    """Get the current status of a container."""
    try:
        container = DockerManager.client.containers.get(container_id)
        return container.status
    except docker.errors.NotFound:
        return "not_found"
    except Exception as e:
        print(f"Error getting container status: {e}")
        return "error"

def delete_llm(deployment_id: str) -> bool:
    """Delete a LLM deployment cleanly."""
    # Get the deployment
    llm = llm_manager.get_by_id(deployment_id)
    if not llm:
        raise HTTPException(status_code=404, detail=f"LLM deployment not found: {deployment_id}")
    
    # Stop and remove the container if it exists
    if hasattr(llm, 'container_id') and llm.container_id:
        try:
            container = DockerManager.client.containers.get(llm.container_id)
            
            # Stop if running
            if container.status == "running":
                container.stop(timeout=30)
            
            # Remove container
            container.remove(force=True)
        except docker.errors.NotFound:
            # Container already gone, continue with deletion
            pass
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to remove container: {str(e)}")
    
    # Remove from state
    llm_manager.delete(deployment_id)
    
    return True
