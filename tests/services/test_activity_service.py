import pytest
from unittest.mock import Mock, AsyncMock
from datetime import datetime, UTC
from fastapi import HTTPException
from app.services.activity_service import ActivityService
from app.schemas.activity import ActivityCreate, ActivityUpdate


@pytest.mark.asyncio
async def test_activity_service_create():
    mock_db = AsyncMock()
    mock_repository = AsyncMock()
    service = ActivityService(mock_db)
    service.repository = mock_repository

    activity_data = ActivityCreate(
        description="Test Activity",
        project_id=1
    )

    mock_project = Mock()
    mock_project.id = 1
    service.project_service.get_project = AsyncMock(return_value=mock_project)

    current_user = Mock()

    await service.create_activity(activity_data, current_user)
    mock_repository.create.assert_called_once()


@pytest.mark.asyncio
async def test_activity_service_get():
    mock_db = AsyncMock()
    mock_repository = AsyncMock()
    service = ActivityService(mock_db)
    service.repository = mock_repository

    mock_activity = Mock()
    mock_repository.get_by_id.return_value = mock_activity

    result = await service.get_activity(1)
    assert result == mock_activity
    mock_repository.get_by_id.assert_called_once_with(1)


@pytest.mark.asyncio
async def test_activity_service_get_not_found():
    mock_db = AsyncMock()
    mock_repository = AsyncMock()
    service = ActivityService(mock_db)
    service.repository = mock_repository

    mock_repository.get_by_id.return_value = None

    with pytest.raises(HTTPException) as exc:
        await service.get_activity(1)
    assert exc.value.status_code == 404
    assert "Activity not found" in exc.value.detail


@pytest.mark.asyncio
async def test_activity_service_list():
    mock_db = AsyncMock()
    mock_repository = AsyncMock()
    service = ActivityService(mock_db)
    service.repository = mock_repository
    mock_repository.get_activities_by_project.return_value = []
    service.project_service.get_project = AsyncMock(return_value=Mock())

    result = await service.get_project_activities(1)
    assert result == []


@pytest.mark.asyncio
async def test_activity_service_update():
    mock_db = AsyncMock()
    mock_repository = AsyncMock()
    service = ActivityService(mock_db)
    service.repository = mock_repository

    activity_data = ActivityUpdate(
        description="Updated Activity",
        end_time=datetime.now(UTC)
    )

    mock_activity = Mock()
    mock_activity.id = 1
    mock_activity.project_id = 1
    mock_repository.get_by_id.return_value = mock_activity

    mock_project = Mock()
    mock_project.id = 1
    service.project_service.get_project = AsyncMock(return_value=mock_project)

    mock_updated = Mock()
    mock_updated.id = 1
    mock_updated.description = "Updated Activity"
    mock_updated.project_id = 1
    mock_updated.start_time = datetime.now(UTC)
    mock_updated.end_time = datetime.now(UTC)
    mock_repository.update.return_value = mock_updated

    result = await service.update_activity(1, activity_data)
    assert result.id == 1
    assert result.description == "Updated Activity"


@pytest.mark.asyncio
async def test_activity_service_delete():
    mock_db = AsyncMock()
    mock_repository = AsyncMock()
    service = ActivityService(mock_db)
    service.repository = mock_repository

    mock_activity = Mock()
    mock_repository.get_by_id.return_value = mock_activity

    result = await service.delete_activity(1)
    assert result is True
    mock_repository.delete.assert_called_once_with(1)
