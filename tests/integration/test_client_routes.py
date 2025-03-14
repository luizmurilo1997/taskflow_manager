"""Integration tests for client routes."""
import pytest
import uuid
from datetime import datetime


@pytest.mark.asyncio
async def test_create_client(test_client):

    unique_id = uuid.uuid4().hex[:8]
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    client_data = {
        "name": f"Test Client {unique_id}",
        "email": f"test_{unique_id}_{timestamp}@example.com",
        "phone": "1234567890"
    }

    headers = {"X-API-Key": "dev_api_key_super_secret"}

    response = await test_client.post(
        "/api/v1/clients/",
        json=client_data,
        headers=headers
    )
    assert response.status_code == 201, f"Error: {response.text}"
    data = response.json()
    assert data["name"] == client_data["name"]
    assert data["email"] == client_data["email"]
    assert "id" in data


@pytest.mark.asyncio
async def test_get_clients(test_client):

    unique_id = uuid.uuid4().hex[:8]
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    client_data = {
        "name": f"Test Client List {unique_id}",
        "email": f"list_{unique_id}_{timestamp}@example.com",
        "phone": "1122334455"
    }

    headers = {"X-API-Key": "dev_api_key_super_secret"}

    await test_client.post(
        "/api/v1/clients/",
        json=client_data,
        headers=headers
    )


    response = await test_client.get(
        "/api/v1/clients/",
        headers=headers
    )
    assert response.status_code == 200, f"Error: {response.text}"
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.asyncio
async def test_get_client_by_id(test_client):

    unique_id = uuid.uuid4().hex[:8]
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    client_data = {
        "name": f"Test Client Get {unique_id}",
        "email": f"get_{unique_id}_{timestamp}@example.com",
        "phone": "0987654321"
    }

    headers = {"X-API-Key": "dev_api_key_super_secret"}

    create_response = await test_client.post(
        "/api/v1/clients/",
        json=client_data,
        headers=headers
    )
    assert create_response.status_code == 201, f"Error: {create_response.text}"
    client_id = create_response.json()["id"]


    response = await test_client.get(
        f"/api/v1/clients/{client_id}",
        headers=headers
    )
    assert response.status_code == 200, f"Error: {response.text}"
    data = response.json()
    assert data["id"] == client_id
    assert data["name"] == client_data["name"]
    assert data["email"] == client_data["email"]


@pytest.mark.asyncio
async def test_update_client(test_client):

    unique_id = uuid.uuid4().hex[:8]
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    client_data = {
        "name": f"Test Client Update {unique_id}",
        "email": f"update_{unique_id}_{timestamp}@example.com",
        "phone": "5566778899"
    }

    headers = {"X-API-Key": "dev_api_key_super_secret"}

    create_response = await test_client.post(
        "/api/v1/clients/",
        json=client_data,
        headers=headers
    )
    assert create_response.status_code == 201, f"Error: {create_response.text}"
    client_id = create_response.json()["id"]

    update_unique_id = uuid.uuid4().hex[:8]
    update_timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    update_data = {
        "name": f"Updated Client {update_unique_id}",
        "email": f"updated_{update_unique_id}_{update_timestamp}@example.com"
    }

    response = await test_client.put(
        f"/api/v1/clients/{client_id}",
        json=update_data,
        headers=headers
    )
    assert response.status_code == 200, f"Error: {response.text}"
    data = response.json()
    assert data["id"] == client_id
    assert data["name"] == update_data["name"]
    assert data["email"] == update_data["email"]
