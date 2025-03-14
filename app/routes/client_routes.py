from fastapi import APIRouter, Depends, HTTPException
from app.schemas.client import ClientCreate, ClientResponse, ClientUpdate
from app.services.client_service import ClientService
from app.core.deps import get_current_client
from typing import List

router = APIRouter(prefix="/api/v1/clients", tags=["Clients"])


@router.post("/", response_model=ClientResponse, status_code=201)
async def create_client(
    client_data: ClientCreate,
    _: bool = Depends(get_current_client),
    service: ClientService = Depends(ClientService)
):
    """
    Registra um novo cliente (empresa) no sistema.

    Args:
        client_data: Dados do cliente a ser criado
        _: Validação da API Key

    Returns:
        Cliente criado

    Raises:
        403 Forbidden: API Key inválida
        409 Conflict: Email já registrado
    """
    return await service.create_client(client_data)


@router.get("/{client_id}", response_model=ClientResponse)
async def get_client(
    client_id: int,
    _: bool = Depends(get_current_client),
    service: ClientService = Depends(ClientService)
):
    """
    Obtém um cliente específico pelo ID.

    Args:
        client_id: ID do cliente a ser recuperado
        _: Validação da API Key

    Returns:
        Cliente se encontrado

    Raises:
        403 Forbidden: API Key inválida
        404 Not Found: Cliente não encontrado
    """
    return await service.get_client(client_id)


@router.put("/{client_id}", response_model=ClientResponse)
async def update_client(
    client_id: int,
    client_data: ClientUpdate,
    _: bool = Depends(get_current_client),
    service: ClientService = Depends(ClientService)
):
    """
    Atualiza as informações de um cliente.

    Args:
        client_id: ID do cliente a ser atualizado
        client_data: Dados atualizados do cliente
        _: Validação da API Key

    Returns:
        Cliente atualizado

    Raises:
        403 Forbidden: API Key inválida
        404 Not Found: Cliente não encontrado
        409 Conflict: Email já em uso
    """
    return await service.update_client(client_id, client_data)


@router.get("/", response_model=List[ClientResponse])
async def get_clients(
    _: bool = Depends(get_current_client),
    service: ClientService = Depends(ClientService)
):
    """
    Lista todos os clientes do sistema.

    Args:
        _: Validação da API Key

    Returns:
        Lista de clientes

    Raises:
        403 Forbidden: API Key inválida
    """
    return await service.get_clients()
