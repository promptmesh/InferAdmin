from fastapi import APIRouter, Query
from .models import (
    GetApplicationsResponse,
    PostApplicationRequest,
    GetApplicationLogsResponse,
    DeleteApplicationRequest,
    ApplicationIdRequest,
)
from .support import (
    get_all_applications,
    deploy_application,
    delete_application,
    get_container_logs,
    stop_container,
    start_container,
)

router = APIRouter(prefix="/applications")


@router.get("/list")
async def get_applications() -> GetApplicationsResponse:
    """Get all applications."""
    applications = get_all_applications()
    return GetApplicationsResponse(applications=applications)


@router.post("/create")
async def post_applications(data: PostApplicationRequest):
    """Deploy a new application."""
    application = await deploy_application(
        name=data.name,
        app_type=data.app_type,
        image_id=data.image_id,
        host_port=data.host_port,
        environment=data.environment,
        gpu_uuids=data.gpu_uuids,
    )
    return application


@router.post("/delete")
async def delete_applications(data: DeleteApplicationRequest) -> bool:
    """Delete an application by its ID."""
    return await delete_application(data.id)


@router.post("/logs")
async def get_application_logs_by_id(data: ApplicationIdRequest, tail: int = Query(100, description="Number of log lines to return")) -> GetApplicationLogsResponse:
    """Get logs for a specific application by its container ID."""
    logs = await get_container_logs(data.id, tail=tail)
    return GetApplicationLogsResponse(id=data.id, logs=logs)


@router.post("/start")
async def start_application(data: ApplicationIdRequest) -> bool:
    """Start a stopped application by its container ID."""
    return await start_container(data.id)


@router.post("/stop")
async def stop_application(data: ApplicationIdRequest) -> bool:
    """Stop a running application by its container ID."""
    return await stop_container(data.id)