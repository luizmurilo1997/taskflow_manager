from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.project import Project
from app.models.client import Client
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.repositories.project_repository import ProjectRepository


class ProjectService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.repository = ProjectRepository(db)

    async def create_project(self, project_data: ProjectCreate, _: Client):
        """
        Create a new project.

        Args:
            project_data: Project data including client_id
            _: API Key validation only
        """
        project_dict = project_data.model_dump()
        return await self.repository.create(project_dict)

    async def get_project(self, project_id: int):
        """
        Retrieve a project by its ID.

        Args:
            project_id: The ID of the project to retrieve

        Raises:
            404 Not Found: If project doesn't exist
        """
        project = await self.repository.get_by_id(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        return project

    async def get_projects(self):
        """
        Retrieve all projects in the system.
        """
        return await self.repository.get_all_projects()

    async def update_project(self, project_id: int, project_data: ProjectUpdate):
        """
        Update a project's information.

        Args:
            project_id: The ID of the project to update
            project_data: New project data

        Raises:
            404 Not Found: If project doesn't exist
        """
        project = await self.get_project(project_id)
        update_data = project_data.model_dump(exclude_unset=True)
        return await self.repository.update(project_id, update_data)

    async def delete_project(self, project_id: int):
        """
        Delete a project.

        Args:
            project_id: The ID of the project to delete

        Raises:
            404 Not Found: If project doesn't exist
        """
        project = await self.get_project(project_id)
        await self.repository.delete(project_id)
        return True
