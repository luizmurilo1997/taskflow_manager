import pytest
from unittest.mock import Mock, AsyncMock
from fastapi import HTTPException
from app.services.client_service import ClientService
from app.schemas.client import ClientCreate, ClientUpdate
from fastapi import status
from datetime import datetime


@pytest.mark.asyncio
async def test_client_service_create():
    mock_db = AsyncMock()
    mock_repository = AsyncMock()
    service = ClientService(mock_db)
    service.repository = mock_repository

    client_data = ClientCreate(
        name="Test Client",
        email="test@example.com",
        password="testpass123"
    )

    mock_repository.get_by_email.return_value = None

    mock_client = Mock()
    mock_client.id = 1
    mock_client.name = "Test Client"
    mock_client.email = "test@example.com"
    mock_repository.create.return_value = mock_client

    result = await service.create_client(client_data)
    assert result.id == 1
    assert result.name == "Test Client"
    assert result.email == "test@example.com"
    mock_repository.create.assert_called_once()


@pytest.mark.asyncio
async def test_client_service_create_duplicate_email():
    mock_db = AsyncMock()
    mock_repository = AsyncMock()
    service = ClientService(mock_db)
    service.repository = mock_repository

    client_data = ClientCreate(
        name="Test Client",
        email="existing@example.com",
        password="testpass123"
    )

    mock_repository.get_by_email.return_value = Mock()

    with pytest.raises(HTTPException) as exc:
        await service.create_client(client_data)
    assert exc.value.status_code == 409
    assert "Email already registered" in exc.value.detail


@pytest.mark.asyncio
async def test_client_service_get():
    mock_db = AsyncMock()
    mock_repository = AsyncMock()
    service = ClientService(mock_db)
    service.repository = mock_repository
    mock_client = Mock()
    mock_repository.get_by_id.return_value = mock_client

    result = await service.get_client(1)
    assert result == mock_client
    mock_repository.get_by_id.assert_called_once_with(1)


@pytest.mark.asyncio
async def test_client_service_get_by_email():
    mock_db = AsyncMock()
    mock_repository = AsyncMock()
    service = ClientService(mock_db)
    service.repository = mock_repository
    mock_client = Mock()
    mock_repository.get_by_email.return_value = mock_client

    result = await service.get_client_by_email("test@example.com")
    assert result == mock_client
    mock_repository.get_by_email.assert_called_once_with("test@example.com")


@pytest.mark.asyncio
async def test_client_service_update():
    mock_db = AsyncMock()
    mock_repository = AsyncMock()
    service = ClientService(mock_db)
    service.repository = mock_repository

    client_data = ClientUpdate(
        name="Updated Client",
        email="updated@example.com"
    )

    mock_client = Mock()
    mock_client.id = 1
    mock_client.name = "Updated Client"
    mock_client.email = "updated@example.com"

    mock_repository.get_by_id.return_value = mock_client
    mock_repository.get_by_email.return_value = None
    mock_repository.update.return_value = mock_client

    result = await service.update_client(1, client_data)
    assert result.id == mock_client.id
    assert result.name == mock_client.name
    assert result.email == mock_client.email


@pytest.mark.asyncio
async def test_client_service_update_not_found():
    mock_db = AsyncMock()
    mock_repository = AsyncMock()
    service = ClientService(mock_db)
    service.repository = mock_repository

    client_data = ClientUpdate(name="Updated Client")
    mock_repository.get_by_id.return_value = None

    with pytest.raises(HTTPException) as exc:
        await service.update_client(1, client_data)
    assert exc.value.status_code == 404
    assert "Client not found" in exc.value.detail


@pytest.mark.asyncio
async def test_client_service_update_duplicate_email():
    mock_db = AsyncMock()
    mock_repository = AsyncMock()
    service = ClientService(mock_db)
    service.repository = mock_repository

    client_data = ClientUpdate(
        email="existing@example.com"
    )

    current_client = Mock()
    current_client.id = 1
    current_client.email = "current@example.com"
    mock_repository.get_by_id.return_value = current_client

    existing_client = Mock()
    existing_client.id = 2
    existing_client.email = "existing@example.com"
    mock_repository.get_by_email.return_value = existing_client

    with pytest.raises(HTTPException) as exc:
        await service.update_client(1, client_data)
    assert exc.value.status_code == 409
    assert "Email already registered" in exc.value.detail


@pytest.mark.asyncio
async def test_client_service_update_other_client():
    mock_db = AsyncMock()
    mock_repository = AsyncMock()
    service = ClientService(mock_db)
    service.repository = mock_repository

    client_data = ClientUpdate(
        name="Attempt to Update Other Client"
    )

    mock_client = Mock()
    mock_client.id = 2
    mock_repository.get_by_id.return_value = mock_client
    mock_repository.update.return_value = mock_client

    current_user = Mock()
    current_user.id = 1

    result = await service.update_client(2, client_data)
    assert result == mock_client


@pytest.mark.asyncio
async def test_client_service_view_other_client():
    mock_db = AsyncMock()
    mock_repository = AsyncMock()
    service = ClientService(mock_db)
    service.repository = mock_repository

    mock_client = Mock()
    mock_client.id = 2
    mock_repository.get_by_id.return_value = mock_client

    current_user = Mock()
    current_user.id = 1

    result = await service.get_client(2)
    assert result == mock_client


@pytest.mark.asyncio
async def test_create_client_duplicate_email_v2():
    """Test creating a client with duplicate email"""
    mock_db = AsyncMock()
    mock_repository = AsyncMock()
    service = ClientService(mock_db)
    service.repository = mock_repository

    client_data = ClientCreate(
        name="Test Company",
        email="test@company.com",
        phone="1234567890"
    )

    mock_existing = Mock()
    mock_existing.email = "test@company.com"
    mock_repository.get_by_email.return_value = mock_existing

    with pytest.raises(HTTPException) as exc_info:
        await service.create_client(client_data)

    assert exc_info.value.status_code == status.HTTP_409_CONFLICT
    assert exc_info.value.detail == "Email already registered"


@pytest.mark.asyncio
async def test_get_client_not_found_v2():
    """Test getting a non-existent client"""
    mock_db = AsyncMock()
    mock_repository = AsyncMock()
    service = ClientService(mock_db)
    service.repository = mock_repository

    mock_repository.get_by_id.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await service.get_client(999)

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == "Client not found"


@pytest.mark.asyncio
async def test_get_clients_list_v2():
    """Test getting all clients using get_clients method"""
    mock_db = AsyncMock()
    mock_repository = AsyncMock()
    service = ClientService(mock_db)
    service.repository = mock_repository

    mock_client1 = Mock()
    mock_client1.email = "company1@test.com"
    mock_client2 = Mock()
    mock_client2.email = "company2@test.com"
    mock_repository.get_all_clients.return_value = [mock_client1, mock_client2]

    clients = await service.get_clients()

    assert len(clients) == 2
    assert any(c.email == "company1@test.com" for c in clients)
    assert any(c.email == "company2@test.com" for c in clients)
    mock_repository.get_all_clients.assert_called_once()


@pytest.mark.asyncio
async def test_list_clients():
    """Test listing all clients with response model validation"""
    mock_db = AsyncMock()
    mock_repository = AsyncMock()
    service = ClientService(mock_db)
    service.repository = mock_repository

    mock_client1 = Mock()
    mock_client1.id = 1
    mock_client1.name = "Company 1"
    mock_client1.email = "company1@test.com"
    mock_client1.phone = "1234567890"
    mock_client1.created_at = datetime.now()
    mock_client1.updated_at = datetime.now()

    mock_client2 = Mock()
    mock_client2.id = 2
    mock_client2.name = "Company 2"
    mock_client2.email = "company2@test.com"
    mock_client2.phone = "0987654321"
    mock_client2.created_at = datetime.now()
    mock_client2.updated_at = datetime.now()

    mock_repository.get_all_clients.return_value = [mock_client1, mock_client2]

    clients = await service.list_clients()

    assert len(clients) == 2
    assert clients[0].email == "company1@test.com"
    assert clients[1].email == "company2@test.com"
    mock_repository.get_all_clients.assert_called_once()
