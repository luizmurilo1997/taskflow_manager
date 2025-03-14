from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.client_repository import ClientRepository
from app.schemas.client import ClientCreate, ClientResponse, ClientUpdate
from fastapi import HTTPException, status, Depends
from app.models.client import Client
from typing import List
from sqlalchemy import select
from app.core.database import get_db


class ClientService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.repository = ClientRepository(db)
        self.db = db

    async def list_clients(self) -> List[ClientResponse]:

        clients = await self.repository.get_all_clients()
        return [ClientResponse.model_validate(client) for client in clients]

    async def create_client(self, client_data: ClientCreate):

        existing_client = await self.repository.get_by_email(client_data.email)
        if existing_client:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )

        client_dict = client_data.model_dump()
        return await self.repository.create(client_dict)

    async def get_client(self, client_id: int):

        client = await self.repository.get_by_id(client_id)
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found"
            )
        return client

    async def get_client_by_email(self, email: str):

        return await self.repository.get_by_email(email)

    async def update_client(self, client_id: int, client_data: ClientUpdate):

        client = await self.repository.get_by_id(client_id)
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found"
            )

        if client_data.email and client_data.email != client.email:
            existing_client = await self.repository.get_by_email(client_data.email)
            if existing_client:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already registered"
                )

        update_data = client_data.model_dump(exclude_unset=True)
        return await self.repository.update(client_id, update_data)

    async def get_clients(self):

        return await self.repository.get_all_clients()
