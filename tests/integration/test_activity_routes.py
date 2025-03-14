"""Integration tests for activity routes."""
import pytest
import uuid
from datetime import datetime


@pytest.mark.asyncio
async def test_create_activity(test_client):
    unique_id = uuid.uuid4().hex[:8]
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    client_data = {
        "name": f"Test Client {unique_id}",
        "email": f"client_{unique_id}_{timestamp}@example.com",
        "phone": "1234567890"
    }

    headers = {"X-API-Key": "dev_api_key_super_secret"}

    client_response = await test_client.post(
        "/api/v1/clients/",
        json=client_data,
        headers=headers
    )
    assert client_response.status_code == 201, f"Error: {client_response.text}"
    client_id = client_response.json()["id"]

    project_data = {
        "name": f"Test Project {unique_id}",
        "description": f"Test Project Description {unique_id}",
        "client_id": client_id
    }

    project_response = await test_client.post(
        "/api/v1/projects/",
        json=project_data,
        headers=headers
    )
    assert project_response.status_code == 201, f"Error: {project_response.text}"
    project_id = project_response.json()["id"]

    activity_data = {
        "description": f"New Activity {unique_id}",
        "project_id": project_id
    }

    activity_response = await test_client.post(
        "/api/v1/activities/",
        json=activity_data,
        headers=headers
    )
    assert activity_response.status_code == 201, f"Error: {activity_response.text}"
    activity_data_response = activity_response.json()
    assert activity_data_response["description"] == activity_data["description"]
    assert activity_data_response["project_id"] == project_id


@pytest.mark.asyncio
async def test_get_activity(test_client):
    
    unique_id = uuid.uuid4().hex[:8]
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    client_data = {
        "name": f"Test Client {unique_id}",
        "email": f"client2_{unique_id}_{timestamp}@example.com",
        "phone": "0987654321"
    }

    headers = {"X-API-Key": "dev_api_key_super_secret"}

    client_response = await test_client.post(
        "/api/v1/clients/",
        json=client_data,
        headers=headers
    )
    assert client_response.status_code == 201, f"Error: {client_response.text}"
    client_id = client_response.json()["id"]

    project_data = {
        "name": f"Test Project {unique_id}",
        "description": f"Test Project Description {unique_id}",
        "client_id": client_id
    }

    project_response = await test_client.post(
        "/api/v1/projects/",
        json=project_data,
        headers=headers
    )
    assert project_response.status_code == 201, f"Error: {project_response.text}"
    project_id = project_response.json()["id"]

    activity_data = {
        "description": f"New Activity {unique_id}",
        "project_id": project_id
    }

    activity_response = await test_client.post(
        "/api/v1/activities/",
        json=activity_data,
        headers=headers
    )
    assert activity_response.status_code == 201, f"Error: {activity_response.text}"
    activity_id = activity_response.json()["id"]

    get_response = await test_client.get(
        f"/api/v1/activities/{activity_id}",
        headers=headers
    )
    assert get_response.status_code == 200, f"Error: {get_response.text}"
    activity_data_response = get_response.json()
    assert activity_data_response["id"] == activity_id
    assert activity_data_response["description"] == activity_data["description"]
    assert activity_data_response["project_id"] == project_id


@pytest.mark.asyncio
async def test_update_activity(test_client):

    unique_id = uuid.uuid4().hex[:8]
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    client_data = {
        "name": f"Test Client {unique_id}",
        "email": f"client3_{unique_id}_{timestamp}@example.com",
        "phone": "5555555555"
    }

    headers = {"X-API-Key": "dev_api_key_super_secret"}

    client_response = await test_client.post(
        "/api/v1/clients/",
        json=client_data,
        headers=headers
    )
    assert client_response.status_code == 201, f"Error: {client_response.text}"
    client_id = client_response.json()["id"]

    project_data = {
        "name": f"Test Project {unique_id}",
        "description": f"Test Project Description {unique_id}",
        "client_id": client_id
    }

    project_response = await test_client.post(
        "/api/v1/projects/",
        json=project_data,
        headers=headers
    )
    assert project_response.status_code == 201, f"Error: {project_response.text}"
    project_id = project_response.json()["id"]

    activity_data = {
        "description": f"New Activity {unique_id}",
        "project_id": project_id
    }

    activity_response = await test_client.post(
        "/api/v1/activities/",
        json=activity_data,
        headers=headers
    )
    assert activity_response.status_code == 201, f"Error: {activity_response.text}"
    activity_id = activity_response.json()["id"]

    update_unique_id = uuid.uuid4().hex[:8]

    update_data = {
        "description": f"Updated Activity {update_unique_id}",
        "end_time": "2023-03-15T14:30:00Z"
    }

    update_response = await test_client.put(
        f"/api/v1/activities/{activity_id}",
        json=update_data,
        headers=headers
    )
    assert update_response.status_code == 200, f"Error: {update_response.text}"
    updated_activity_data = update_response.json()

    assert updated_activity_data["description"] == update_data["description"]
    assert updated_activity_data["id"] == activity_id
    assert "end_time" in updated_activity_data
