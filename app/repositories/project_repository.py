from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.project import Project


class ProjectRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_projects(self):
        query = select(Project)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_projects_by_client(self, client_id: int):
        query = select(Project).filter(Project.client_id == client_id)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_by_id(self, project_id: int):
        query = select(Project).filter(Project.id == project_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create(self, project_data: dict):
        db_project = Project(**project_data)
        self.db.add(db_project)
        await self.db.commit()
        await self.db.refresh(db_project)
        return db_project

    async def update(self, project_id: int, update_data: dict):
        project = await self.get_by_id(project_id)
        if project:
            for key, value in update_data.items():
                setattr(project, key, value)
            await self.db.commit()
            await self.db.refresh(project)
        return project
