import docker
from typing import Dict
from fastapi import HTTPException
from datetime import datetime
from uuid import uuid4

from inferadmin.docker import DockerManager
from inferadmin.state.manager import StateManager
from inferadmin.state import STATE_DIR
from inferadmin.routes.deployments.applications.models import Application
from inferadmin.routes.images.support import get_image_name_by_id

# Create state manager for applications
app_manager = StateManager(STATE_DIR, "applications.json", Application)

def deploy_application(name: str, app_type: str, image_id: str, host_port: int, 
                      environment: Dict[str, str] = None, gpu_uuids: list[str] = None) -> Application:
    """Deploy an application container with explicit configuration."""
    try:
        image_name = get_image_name_by_id(image_id)
        
        # Set up container configuration
        ports = {}
        volumes = {}
        env = environment or {}
        device_requests = None
        
        # Configure based on application type
        if app_type == "OpenWebUI":
            # Map container port to host port
            ports = {'3000/tcp': ('0.0.0.0', host_port)}
            
            # Set required environment variables
            env.update({
                'WEBUI_ALLOW_DOWNLOADS': 'true'
            })

            # Add default volume mapping per quick start
            volumes = {'open-webui': {'bind': '/app/backend/data', 'mode': 'rw'}}

        elif app_type == "vLLM":
            raise HTTPException(status_code=400, detail="vLLM application type is not supported yet.")
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported application type: {app_type}")

        # Add attach GPUs if GPU UUIDs are specified
        if gpu_uuids:
            device_requests = [
                docker.types.DeviceRequest(
                    device_ids=gpu_uuids,
                    capabilities=[['gpu']]
                )
            ]

        # Launch container
        container = DockerManager.client.containers.run(
            image_name,
            detach=True,
            environment=env,
            ports=ports,
            volumes=volumes,
            name=f"inferadmin-app-{name}",
            labels={
                "managed-by": "inferadmin",
                "deployment-type": "application",
            },
            device_requests=device_requests
        )
        
        # Create application record
        application = Application(
            id=container.id,
            name=name,
            state="starting",
            type=app_type,
            deployed=datetime.now(),
            host_port=host_port
        )
        
        # Save to state
        app_manager.add(application)
        
        return application
        
    except docker.errors.ImageNotFound:
        raise HTTPException(status_code=404, detail=f"Application image not found for type: {app_type}")
    except docker.errors.APIError as e:
        raise HTTPException(status_code=500, detail=f"Docker API error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to deploy application: {str(e)}")

def get_all_applications() -> list[Application]:
    """Get all applications with current status and logs."""
    applications = app_manager.get_all()
    
    # Update status for each application
    for app in applications:
        if hasattr(app, 'id') and app.id:
            app.state = get_container_status(app.id)

    return applications

def get_container_status(id: str) -> str:
    """Get the current status of a container."""
    try:
        container = DockerManager.client.containers.get(id)
        return container.status
    except docker.errors.NotFound:
        return "not_found"
    except Exception as e:
        print(f"Error getting container status: {e}")
        return "error"

def delete_application(deployment_id: str) -> bool:
    """Delete an application cleanly."""
    # Get the deployment
    application = app_manager.get_by_id(deployment_id)
    if not application:
        raise HTTPException(status_code=404, detail=f"Application not found: {deployment_id}")
    
    # Stop and remove the container if it exists
    if hasattr(application, 'id') and application.id:
        try:
            container = DockerManager.client.containers.get(application.id)
            
            # Stop if running
            if container.status == "running":
                container.stop(timeout=10)
            
            # Remove container
            container.remove(force=True) # does not kill volumes
        except docker.errors.NotFound:
            # Container already gone, continue with deletion
            pass
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to remove container: {str(e)}")
    
    # Remove from state
    app_manager.delete(deployment_id)
    
    return True

def get_container_logs(id: str) -> str:
    """Retrieve logs of a container."""
    try:
        container = DockerManager.client.containers.get(id)
        logs = container.logs(follow=False).decode('utf-8')
        # update application logs in state
        application = app_manager.get_by_id(id)
        if application:
            application.logs = logs
            app_manager.update(application)
        return 
    except docker.errors.NotFound:
        raise HTTPException(status_code=404, detail=f"Container not found: {id}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve logs: {str(e)}")

def stop_container(id: str) -> bool:
    """Stop a running container."""
    try:
        container = DockerManager.client.containers.get(id)
        if container.status == "running":
            container.stop(timeout=10)
        return True
    except docker.errors.NotFound:
        raise HTTPException(status_code=404, detail=f"Container not found: {id}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to stop container: {str(e)}")

def start_container(id: str) -> bool:
    """Start an existing container."""
    try:
        container = DockerManager.client.containers.get(id)
        if container.status != "running":
            container.start()
        return True
    except docker.errors.NotFound:
        raise HTTPException(status_code=404, detail=f"Container not found: {id}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start container: {str(e)}")
