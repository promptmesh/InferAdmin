from typing import Dict
from fastapi import HTTPException
from datetime import datetime
from loguru import logger

from inferadmin.docker import DockerManager
from inferadmin.common.container_management import (
    get_container_logs as get_logs,
    get_container_status,
    stop_container as stop_container_base,
    start_container as start_container_base,
    run_container,
)
from inferadmin.state.manager import StateManager
from inferadmin.state import STATE_DIR
from .models import Application

# Create state manager for applications
app_manager = StateManager(STATE_DIR, "applications.json", Application)


async def deploy_application(
    name: str,
    app_type: str,
    image_id: str,
    host_port: int,
    environment: Dict[str, str] = None,
    gpu_uuids: list[str] = None,
) -> Application:
    """Deploy an application container with explicit configuration."""
    ports = {}
    volumes = {}
    env = environment or {}
    labels = {
        "deployment-type": "application",
    }

    # Configure based on application type
    if app_type == "OpenWebUI":
        # Map container port to host port
        ports = {"3000/tcp": ("0.0.0.0", host_port)}
        # Set required environment variables
        env.update({"WEBUI_ALLOW_DOWNLOADS": "true"})
        # Add default volume mapping per quick start
        volumes = {"open-webui": {"bind": "/app/backend/data", "mode": "rw"}}
    elif app_type == "vLLM":
        raise HTTPException(
            status_code=400, detail="vLLM application type is not supported yet."
        )
    else:
        raise HTTPException(
            status_code=400, detail=f"Unsupported application type: {app_type}"
        )
    try:
        # Launch container using common utility
        container = await run_container(
            image_id=image_id,
            name=f"inferadmin-app-{name}",
            ports=ports,
            volumes=volumes,
            environment=env,
            gpu_uuids=gpu_uuids,
            labels=labels,
        )

        # Create application record
        application = Application(
            id=container.id,
            name=name,
            state="starting",
            type=app_type,
            deployed=datetime.now(),
            host_port=host_port,
            gpu_uuids=gpu_uuids,
        )

        # Save to state
        app_manager.add(application)

        return application

    except Exception as e:
        # Common utility already handles specific exceptions
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=500, detail=f"Failed to deploy application: {str(e)}"
        )


def get_all_applications() -> list[Application]:
    """Get all applications with current status."""
    applications = app_manager.get_all()

    # Early return if no applications
    if not applications:
        return applications

    # Collect all container IDs
    container_ids = [app.id for app in applications if hasattr(app, "id") and app.id]
    
    # If we have container IDs, get their statuses efficiently
    if container_ids:
        try:
            # Get all containers at once
            containers = DockerManager.client.containers.list(all=True, filters={"id": container_ids})
            
            # Create a map of container ID to status
            container_status = {
                container.id: container.status for container in containers
            }
            
            # Update application statuses
            for app in applications:
                if hasattr(app, "id") and app.id:
                    # Use status from map or "not_found" if container no longer exists
                    app.state = container_status.get(app.id, "not_found")
        except Exception as e:
            logger.error(f"fetching container statuses: {e}")
            # Fall back to individual status checks if batch operation fails
            for app in applications:
                if hasattr(app, "id") and app.id:
                    app.state = get_container_status(app.id)

    return applications


async def delete_application(deployment_id: str) -> bool:
    """Delete an application cleanly."""
    # Get the deployment
    application = app_manager.get_by_id(deployment_id)
    if not application:
        raise HTTPException(
            status_code=404, detail=f"Application not found: {deployment_id}"
        )

    # Stop and remove the container if it exists
    if hasattr(application, "id") and application.id:
        try:
            container = DockerManager.client.containers.get(application.id)
            
            # Stop if running
            if container.status == "running":
                await stop_container_base(application.id)
                
            # Remove container
            container.remove(force=True)  # does not kill volumes
        except Exception as e:
            # If it's already a HTTPException, re-raise it
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(
                status_code=500, detail=f"Failed to remove container: {str(e)}"
            )

    # Remove from state
    app_manager.delete(deployment_id)
    return True


async def get_container_logs(id: str, tail: int = 100) -> str:
    """
    Retrieve logs of a container and update application state.
    
    Args:
        id: Container ID
        tail: Number of log lines to return (default: 100)
    """
    logs = await get_logs(id, tail=tail)
    
    # Update logs in application state if it exists
    application = app_manager.get_by_id(id)
    if application:
        application.logs = logs
        app_manager.update(application)
    
    return logs


async def stop_container(id: str) -> bool:
    """Stop a running container."""
    return await stop_container_base(id)


async def start_container(id: str) -> bool:
    """Start an existing container."""
    return await start_container_base(id)