from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.models.activity import Activity
from app.models.project import Project


class ActivityRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_activities(self):
        query = select(Activity)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_activities_by_client(self, client_id: int):
        query = select(Activity).join(Project).filter(
            Project.client_id == client_id)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_activities_by_project(self, project_id: int):
        query = select(Activity).filter(Activity.project_id == project_id)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_by_id(self, activity_id: int):
        query = select(Activity).filter(Activity.id == activity_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create(self, activity_data: dict):
        db_activity = Activity(**activity_data)
        self.db.add(db_activity)
        await self.db.commit()
        await self.db.refresh(db_activity)
        return db_activity

    async def update(self, activity_id: int, update_data: dict):
        activity = await self.get_by_id(activity_id)
        if activity:
            for key, value in update_data.items():
                setattr(activity, key, value)
            await self.db.commit()
            await self.db.refresh(activity)
        return activity

    async def delete(self, activity_id: int):
        query = delete(Activity).where(Activity.id == activity_id)
        await self.db.execute(query)
        await self.db.commit()
