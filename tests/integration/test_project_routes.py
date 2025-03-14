"""Integration tests for project routes."""
import pytest
import uuid
from datetime import datetime


@pytest.mark.asyncio
async def test_create_project(test_client):

    unique_id = uuid.uuid4().hex[:8]
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    client_data = {
        "name": f"Test Client {unique_id}",
        "email": f"test_{unique_id}_{timestamp}@example.com",
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

    response = await test_client.post(
        "/api/v1/projects/",
        json=project_data,
        headers=headers
    )
    assert response.status_code == 201, f"Error: {response.text}"
    data = response.json()
    assert data["name"] == project_data["name"]
    assert data["description"] == project_data["description"]
    assert data["client_id"] == client_id


@pytest.mark.asyncio
async def test_get_projects(test_client):

    unique_id = uuid.uuid4().hex[:8]
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    client_data = {
        "name": f"Test Client List {unique_id}",
        "email": f"list_{unique_id}_{timestamp}@example.com",
        "phone": "1122334455"
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
        "name": f"Test Project List {unique_id}",
        "description": f"Project for list test {unique_id}",
        "client_id": client_id
    }

    await test_client.post(
        "/api/v1/projects/",
        json=project_data,
        headers=headers
    )

    response = await test_client.get(
        "/api/v1/projects/",
        headers=headers
    )
    assert response.status_code == 200, f"Error: {response.text}"
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.asyncio
async def test_get_project_by_id(test_client):
    unique_id = uuid.uuid4().hex[:8]
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    client_data = {
        "name": f"Test Client Get {unique_id}",
        "email": f"get_{unique_id}_{timestamp}@example.com",
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
        "name": f"Test Project Get {unique_id}",
        "description": f"Project for get test {unique_id}",
        "client_id": client_id
    }

    project_response = await test_client.post(
        "/api/v1/projects/",
        json=project_data,
        headers=headers
    )
    assert project_response.status_code == 201, f"Error: {project_response.text}"
    project_id = project_response.json()["id"]


    response = await test_client.get(
        f"/api/v1/projects/{project_id}",
        headers=headers
    )
    assert response.status_code == 200, f"Error: {response.text}"
    data = response.json()
    assert data["id"] == project_id
    assert data["name"] == project_data["name"]
    assert data["client_id"] == client_id


@pytest.mark.asyncio
async def test_update_project(test_client):

    unique_id = uuid.uuid4().hex[:8]
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    client_data = {
        "name": f"Test Client Update {unique_id}",
        "email": f"update_{unique_id}_{timestamp}@example.com",
        "phone": "5566778899"
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
        "name": f"Test Project Update {unique_id}",
        "description": f"Project for update test {unique_id}",
        "client_id": client_id
    }

    project_response = await test_client.post(
        "/api/v1/projects/",
        json=project_data,
        headers=headers
    )
    assert project_response.status_code == 201, f"Error: {project_response.text}"
    project_id = project_response.json()["id"]

    update_unique_id = uuid.uuid4().hex[:8]

    update_data = {
        "name": f"Updated Project {update_unique_id}",
        "description": f"Updated description {update_unique_id}",
        "status": "In Progress"
    }

    response = await test_client.put(
        f"/api/v1/projects/{project_id}",
        json=update_data,
        headers=headers
    )
    assert response.status_code == 200, f"Error: {response.text}"
    data = response.json()
    assert data["id"] == project_id
    assert data["name"] == update_data["name"]
    assert data["description"] == update_data["description"]
    assert data["status"] == update_data["status"]
