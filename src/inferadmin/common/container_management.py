import docker
import secrets
from fastapi import HTTPException
from typing import Dict, List, Any

from inferadmin.docker import DockerManager
from inferadmin.routes.images.support import get_image_name_by_id


def generate_deployment_id() -> str:
    """Generate a unique ID for a deployment."""
    return secrets.token_hex(4)


def check_container_exists(container_id: str) -> bool:
    """Check if a Docker container exists."""
    try:
        DockerManager.client.containers.get(container_id)
        return True
    except docker.errors.NotFound:
        return False
    except Exception as e:
        print(f"Error checking container: {e}")
        return False


def get_container_status(container_id: str) -> str:
    """Get the status of a Docker container."""
    try:
        container = DockerManager.client.containers.get(container_id)
        return container.status
    except docker.errors.NotFound:
        return "not_found"
    except Exception as e:
        print(f"Error getting container status: {e}")
        return "error"


def stop_container(container_id: str) -> bool:
    """Stop a Docker container."""
    try:
        container = DockerManager.client.containers.get(container_id)
        if container.status == "running":
            container.stop(timeout=10)  # Give 10 seconds for graceful shutdown
        return True
    except docker.errors.NotFound:
        raise HTTPException(status_code=404, detail=f"Container not found: {container_id}")
    except Exception as e:
        print(f"Error stopping container: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to stop container: {str(e)}"
        )


def start_container(container_id: str) -> bool:
    """Start a Docker container."""
    try:
        container = DockerManager.client.containers.get(container_id)
        if container.status != "running":
            container.start()
        return True
    except docker.errors.NotFound:
        raise HTTPException(status_code=404, detail=f"Container not found: {container_id}")
    except Exception as e:
        print(f"Error starting container: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to start container: {str(e)}"
        )


def remove_container(container_id: str) -> bool:
    """Remove a Docker container."""
    try:
        container = DockerManager.client.containers.get(container_id)
        container.remove(force=True)
        return True
    except docker.errors.NotFound:
        return False
    except Exception as e:
        print(f"Error removing container: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to remove container: {str(e)}"
        )


def get_container_logs(container_id: str, tail: int = 100) -> str:
    """Get logs from a Docker container."""
    try:
        container = DockerManager.client.containers.get(container_id)
        logs = container.logs(tail=tail, timestamps=True).decode("utf-8")
        return logs
    except docker.errors.NotFound:
        raise HTTPException(
            status_code=404, detail=f"Container {container_id} not found"
        )
    except Exception as e:
        print(f"Error getting container logs: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to get container logs: {str(e)}"
        )


def run_container(
    image_id: str,
    name: str,
    ports: Dict[str, Any] = None,
    volumes: Dict[str, Any] = None,
    environment: Dict[str, str] = None,
    gpu_uuids: List[str] = None,
    labels: Dict[str, str] = None,
) -> docker.models.containers.Container:
    """
    Run a docker container with the specified configuration.
    
    Args:
        image_id: The ID or name of the Docker image to run
        name: Name to assign to the container
        ports: Port mapping configuration
        volumes: Volume mapping configuration 
        environment: Environment variables to set in the container
        gpu_uuids: List of GPU UUIDs to attach to the container
        labels: Labels to apply to the container
        
    Returns:
        The created container
    """
    try:
        image_name = get_image_name_by_id(image_id)
        
        # Set up default parameters
        ports = ports or {}
        volumes = volumes or {}
        env = environment or {}
        labels = labels or {}
        device_requests = None
        
        # Add standard labels
        labels.update({
            "managed-by": "inferadmin",
        })
        
        # Configure GPU access if requested
        if gpu_uuids:
            device_requests = [
                docker.types.DeviceRequest(device_ids=gpu_uuids, capabilities=[["gpu"]])
            ]
            
        # Launch container
        container = DockerManager.client.containers.run(
            image_name,
            detach=True,
            environment=env,
            ports=ports,
            volumes=volumes,
            name=name,
            labels=labels,
            device_requests=device_requests,
        )
        
        return container
        
    except docker.errors.ImageNotFound:
        raise HTTPException(status_code=404, detail=f"Image not found: {image_id}")
    except docker.errors.APIError as e:
        raise HTTPException(status_code=500, detail=f"Docker API error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error running container: {str(e)}")