import pytest
from unittest.mock import Mock, AsyncMock
from datetime import datetime, UTC
from fastapi import HTTPException
from app.services.project_service import ProjectService
from app.schemas.project import ProjectCreate, ProjectUpdate


@pytest.mark.asyncio
async def test_project_service_create():
    mock_db = AsyncMock()
    mock_repository = AsyncMock()
    service = ProjectService(mock_db)
    service.repository = mock_repository

    project_data = ProjectCreate(
        name="Test Project",
        description="Test",
        client_id=1
    )

    current_user = Mock()

    await service.create_project(project_data, current_user)
    mock_repository.create.assert_called_once()


@pytest.mark.asyncio
async def test_project_service_get():
    mock_db = AsyncMock()
    mock_repository = AsyncMock()
    service = ProjectService(mock_db)
    service.repository = mock_repository

    mock_project = Mock()
    mock_repository.get_by_id.return_value = mock_project

    result = await service.get_project(1)
    assert result == mock_project
    mock_repository.get_by_id.assert_called_once_with(1)


@pytest.mark.asyncio
async def test_project_service_get_not_found():
    mock_db = AsyncMock()
    mock_repository = AsyncMock()
    service = ProjectService(mock_db)
    service.repository = mock_repository

    mock_repository.get_by_id.return_value = None

    with pytest.raises(HTTPException) as exc:
        await service.get_project(1)
    assert exc.value.status_code == 404
    assert "Project not found" in exc.value.detail


@pytest.mark.asyncio
async def test_project_service_list():
    mock_db = AsyncMock()
    mock_repository = AsyncMock()
    service = ProjectService(mock_db)
    service.repository = mock_repository
    mock_repository.get_all_projects.return_value = []

    result = await service.get_projects()
    assert isinstance(result, list)
    mock_repository.get_all_projects.assert_called_once()


@pytest.mark.asyncio
async def test_project_service_update():
    mock_db = AsyncMock()
    mock_repository = AsyncMock()
    service = ProjectService(mock_db)
    service.repository = mock_repository

    project_data = ProjectUpdate(
        name="Updated Project",
        description="Updated description"
    )

    mock_project = Mock()
    mock_project.id = 1
    mock_project.name = "Updated Project"
    mock_project.description = "Updated description"
    mock_project.status = "Open"
    mock_project.client_id = 1

    mock_repository.get_by_id.return_value = mock_project
    mock_repository.update.return_value = mock_project

    result = await service.update_project(1, project_data)
    assert result.id == mock_project.id
    assert result.name == mock_project.name
    assert result.description == mock_project.description
    assert result.status == mock_project.status
    assert result.client_id == mock_project.client_id


@pytest.mark.asyncio
async def test_project_service_delete():
    mock_db = AsyncMock()
    mock_repository = AsyncMock()
    service = ProjectService(mock_db)
    service.repository = mock_repository

    mock_project = Mock()
    mock_repository.get_by_id.return_value = mock_project

    result = await service.delete_project(1)
    assert result is True
    mock_repository.delete.assert_called_once_with(1)
