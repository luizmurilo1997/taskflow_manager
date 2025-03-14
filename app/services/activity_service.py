from app.repositories.activity_repository import ActivityRepository
from app.schemas.activity import ActivityCreate, ActivityResponse, ActivityUpdate
from typing import List
from fastapi import HTTPException, status, Depends
from app.models.client import Client
from app.services.project_service import ProjectService
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db


class ActivityService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.repository = ActivityRepository(db)
        self.project_service = ProjectService(db)

    async def create_activity(self, activity_data: ActivityCreate, current_user: Client):
        # Verificar se o projeto existe
        project = await self.project_service.get_project(activity_data.project_id)

        # Preparar dados da atividade
        activity_dict = activity_data.model_dump()
        activity_dict["start_time"] = activity_dict.get(
            "start_time") or datetime.now(timezone.utc)

        # Criar a atividade usando o repository
        return await self.repository.create(activity_dict)

    async def get_activity(self, activity_id: int):
        activity = await self.repository.get_by_id(activity_id)
        if not activity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Activity not found"
            )
        return activity

    async def get_project_activities(self, project_id: int):
        # Verificar se o projeto existe
        await self.project_service.get_project(project_id)
        return await self.repository.get_activities_by_project(project_id)

    async def update_activity(self, activity_id: int, activity_data: ActivityUpdate):
        # Verificar se a atividade existe
        activity = await self.get_activity(activity_id)

        # Atualizar usando o repository
        update_data = activity_data.model_dump(exclude_unset=True)
        return await self.repository.update(activity_id, update_data)

    async def delete_activity(self, activity_id: int):
        # Verificar se a atividade existe
        activity = await self.get_activity(activity_id)

        # Deletar usando o repository
        await self.repository.delete(activity_id)
        return True
