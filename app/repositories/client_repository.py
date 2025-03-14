from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.client import Client


class ClientRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_email(self, email: str) -> Client | None:
        """
        Busca um cliente pelo email
        """
        query = select(Client).filter(Client.email == email)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_api_key(self, api_key: str) -> Client | None:
        """
        Busca um cliente pela API Key
        """
        query = select(Client).filter(Client.api_key == api_key)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_id(self, client_id: int):
        query = select(Client).filter(Client.id == client_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create(self, client_data: dict) -> Client:
        db_client = Client(**client_data)
        self.db.add(db_client)
        await self.db.commit()
        await self.db.refresh(db_client)
        return db_client

    async def get_all_clients(self) -> list[Client]:
        query = select(Client)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def update(self, client_id: int, update_data: dict):
        client = await self.get_by_id(client_id)
        if client:
            for key, value in update_data.items():
                setattr(client, key, value)
            await self.db.commit()
            await self.db.refresh(client)
        return client
