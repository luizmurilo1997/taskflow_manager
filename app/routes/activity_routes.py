from fastapi import APIRouter, Depends
from app.schemas.activity import ActivityCreate, ActivityResponse, ActivityUpdate
from app.services.activity_service import ActivityService
from app.core.deps import get_current_client
from app.models.client import Client
from typing import List

router = APIRouter(prefix="/api/v1/activities", tags=["Activities"])


@router.post("/", response_model=ActivityResponse, status_code=201)
async def create_activity(
    activity_data: ActivityCreate,
    current_client: Client = Depends(get_current_client),
    service: ActivityService = Depends(ActivityService)
):
    """
    Create a new activity for a project.

    Args:
        activity_data: Activity data to create
        current_client: Client authenticated via API Key
        service: Activity service

    Returns:
        Created activity

    Raises:
        403 Forbidden: Invalid API Key
        404 Not Found: Project not found
    """
    return await service.create_activity(activity_data, current_client)


@router.get("/project/{project_id}", response_model=List[ActivityResponse])
async def get_project_activities(
    project_id: int,
    _: Client = Depends(get_current_client),
    service: ActivityService = Depends(ActivityService)
):
    """
    Get all activities for a specific project.

    Args:
        project_id: ID of the project
        _: Client authenticated via API Key (apenas para validação)
        service: Activity service

    Returns:
        List of activities

    Raises:
        403 Forbidden: Invalid API Key
        404 Not Found: Project not found
    """
    return await service.get_project_activities(project_id)


@router.get("/{activity_id}", response_model=ActivityResponse)
async def get_activity(
    activity_id: int,
    _: Client = Depends(get_current_client),
    service: ActivityService = Depends(ActivityService)
):
    """
    Get a specific activity by ID.

    Args:
        activity_id: ID of the activity to retrieve
        _: Client authenticated via API Key (apenas para validação)
        service: Activity service

    Returns:
        Activity if found

    Raises:
        403 Forbidden: Invalid API Key
        404 Not Found: Activity not found
    """
    return await service.get_activity(activity_id)


@router.put("/{activity_id}", response_model=ActivityResponse)
async def update_activity(
    activity_id: int,
    activity_data: ActivityUpdate,
    _: Client = Depends(get_current_client),
    service: ActivityService = Depends(ActivityService)
):
    """
    Update an activity.

    Args:
        activity_id: ID of the activity to update
        activity_data: Updated activity data
        _: Client authenticated via API Key (apenas para validação)
        service: Activity service

    Returns:
        Updated activity

    Raises:
        403 Forbidden: Invalid API Key
        404 Not Found: Activity not found
    """
    return await service.update_activity(activity_id, activity_data)


@router.delete("/{activity_id}", status_code=204)
async def delete_activity(
    activity_id: int,
    _: Client = Depends(get_current_client),
    service: ActivityService = Depends(ActivityService)
):
    """
    Delete an activity.

    Args:
        activity_id: ID of the activity to delete
        _: Client authenticated via API Key (apenas para validação)
        service: Activity service

    Raises:
        403 Forbidden: Invalid API Key
        404 Not Found: Activity not found
    """
    await service.delete_activity(activity_id)
