import docker
from typing import Dict
from fastapi import HTTPException
from datetime import datetime
from uuid import uuid4

from inferadmin.docker import DockerManager
from inferadmin.state.manager import StateManager
from inferadmin.state import STATE_DIR
from inferadmin.routes.deployments.applications.models import Applications
from inferadmin.routes.images.support import get_container_images

# Create state manager for applications
app_manager = StateManager(STATE_DIR, "applications.json", Applications)

def deploy_application(name: str, app_type: str, host_port: int, api_url: str = None, 
                      environment: Dict[str, str] = None) -> Applications:
    """Deploy an application container with explicit configuration."""
    try:
        # Generate unique ID
        deployment_id = str(uuid4())[:8]
        
        # Get the image for this application type
        image_name = get_image_for_app_type(app_type)
        
        # Set up container configuration
        ports = {}
        volumes = {}
        env = environment or {}
        
        # Configure based on application type
        if app_type == "OpenWebUI":
            # Map container port to host port
            ports = {'3000/tcp': ('0.0.0.0', host_port)}
            
            # Set required environment variables
            env.update({
                'WEBUI_ALLOW_DOWNLOADS': 'true'
            })
            
            # Add API URL if provided for connecting to LLM
            if api_url:
                env['OLLAMA_BASE_URL'] = api_url
        
        # Launch container
        container = DockerManager.client.containers.run(
            image_name,
            detach=True,
            environment=env,
            ports=ports,
            volumes=volumes,
            name=f"inferadmin-app-{deployment_id}",
            labels={
                "managed-by": "inferadmin",
                "deployment-type": "application",
                "deployment-id": deployment_id
            }
        )
        
        # Create application record
        application = Applications(
            id=deployment_id,
            name=name,
            state="starting",
            type=app_type,
            deployed=datetime.now(),
            container_id=container.id,
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

def get_image_for_app_type(app_type: str) -> str:
    """Get Docker image name for an application type."""
    image_mapping = {
        "OpenWebUI": "ghcr.io/open-webui/open-webui:main"
    }
    
    if app_type not in image_mapping:
        raise HTTPException(status_code=400, detail=f"Unsupported application type: {app_type}")
    
    return image_mapping[app_type]

def get_all_applications() -> list[Applications]:
    """Get all applications with current status."""
    applications = app_manager.get_all()
    
    # Update status for each application
    for app in applications:
        if hasattr(app, 'container_id') and app.container_id:
            app.state = get_container_status(app.container_id)
    
    return applications

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

def delete_application(deployment_id: str) -> bool:
    """Delete an application cleanly."""
    # Get the deployment
    application = app_manager.get_by_id(deployment_id)
    if not application:
        raise HTTPException(status_code=404, detail=f"Application not found: {deployment_id}")
    
    # Stop and remove the container if it exists
    if hasattr(application, 'container_id') and application.container_id:
        try:
            container = DockerManager.client.containers.get(application.container_id)
            
            # Stop if running
            if container.status == "running":
                container.stop(timeout=10)
            
            # Remove container
            container.remove(force=True)
        except docker.errors.NotFound:
            # Container already gone, continue with deletion
            pass
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to remove container: {str(e)}")
    
    # Remove from state
    app_manager.delete(deployment_id)
    
    return True
