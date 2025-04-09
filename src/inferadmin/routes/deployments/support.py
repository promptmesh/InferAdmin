import docker
import uuid
from fastapi import HTTPException

from inferadmin.docker import DockerManager


def generate_deployment_id() -> str:
    """Generate a unique ID for a deployment."""
    return str(uuid.uuid4())[:8]


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
        container.stop(timeout=10)  # Give 10 seconds for graceful shutdown
        return True
    except docker.errors.NotFound:
        return False
    except Exception as e:
        print(f"Error stopping container: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to stop container: {str(e)}"
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


def update_deployment_status(deployment_manager, deployment_id: str) -> bool:
    """Update the status of a deployment."""
    deployment = deployment_manager.get_by_id(deployment_id)
    if not deployment:
        return False

    container_id = getattr(deployment, "container_id", None)
    if not container_id:
        return False

    # Update container status
    status = get_container_status(container_id)
    deployment.status = status
    deployment_manager.update(deployment)
    return True
