from fastapi import APIRouter, Depends
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.services.project_service import ProjectService
from app.core.deps import get_current_client
from typing import List

router = APIRouter(prefix="/api/v1/projects", tags=["Projects"])


@router.post("/", response_model=ProjectResponse, status_code=201)
async def create_project(
    project_data: ProjectCreate,
    _: bool = Depends(get_current_client),
    service: ProjectService = Depends(ProjectService)
):
    """
    Create a new project for a specific client.

    Args:
        project_data: Project data including name, description, status, and client_id
        _: API Key validation

    Returns:
        Created project with all its details

    Raises:
        403 Forbidden: Invalid API Key
        404 Not Found: Client not found
        422 Unprocessable Entity: Invalid project data
    """
    return await service.create_project(project_data, _)


@router.get("/", response_model=List[ProjectResponse])
async def get_projects(
    _: bool = Depends(get_current_client),
    service: ProjectService = Depends(ProjectService)
):
    """
    Retrieve all projects in the system.

    Args:
        _: API Key validation

    Returns:
        List of all projects with their details

    Raises:
        403 Forbidden: Invalid API Key
    """
    return await service.get_projects()


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    _: bool = Depends(get_current_client),
    service: ProjectService = Depends(ProjectService)
):
    """
    Retrieve a specific project by its ID.

    Args:
        project_id: The ID of the project to retrieve
        _: API Key validation

    Returns:
        Project details if found

    Raises:
        403 Forbidden: Invalid API Key
        404 Not Found: Project not found
    """
    return await service.get_project(project_id)


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    _: bool = Depends(get_current_client),
    service: ProjectService = Depends(ProjectService)
):
    """
    Update a specific project's information.

    Args:
        project_id: The ID of the project to update
        project_data: Updated project data (name, description, status)
        _: API Key validation

    Returns:
        Updated project details

    Raises:
        403 Forbidden: Invalid API Key
        404 Not Found: Project not found
        422 Unprocessable Entity: Invalid update data
    """
    return await service.update_project(project_id, project_data)


@router.delete("/{project_id}", status_code=204)
async def delete_project(
    project_id: int,
    _: bool = Depends(get_current_client),
    service: ProjectService = Depends(ProjectService)
):
    """
    Delete a specific project.

    Args:
        project_id: The ID of the project to delete
        _: API Key validation

    Raises:
        403 Forbidden: Invalid API Key
        404 Not Found: Project not found
    """
    await service.delete_project(project_id)
