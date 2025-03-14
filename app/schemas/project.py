from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import datetime


class ProjectStatus(str, Enum):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    status: ProjectStatus = ProjectStatus.OPEN
    client_id: int

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Sistema de Gestão",
                    "description": "Desenvolvimento de sistema de gestão empresarial",
                    "status": "Open",
                    "client_id": 1
                }
            ]
        }
    }


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Sistema de Gestão v2",
                    "description": "Atualização do sistema de gestão empresarial",
                    "status": "In Progress"
                }
            ]
        }
    }


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    status: ProjectStatus
    client_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "name": "Sistema de Gestão",
                    "description": "Desenvolvimento de sistema de gestão empresarial",
                    "status": "Open",
                    "client_id": 1,
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-01T00:00:00Z"
                }
            ]
        }
    }
