from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ActivityCreate(BaseModel):
    description: str
    project_id: int
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "description": "Implementação do módulo de autenticação",
                    "project_id": 1,
                    "start_time": "2024-03-13T10:00:00Z",
                    "end_time": None
                }
            ]
        }
    }


class ActivityUpdate(BaseModel):
    description: Optional[str] = None
    end_time: Optional[datetime] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "description": "Implementação do módulo de autenticação - Concluído",
                    "end_time": "2024-03-13T12:00:00Z"
                }
            ]
        }
    }


class ActivityResponse(BaseModel):
    id: int
    description: str
    project_id: int
    start_time: datetime
    end_time: Optional[datetime]

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "description": "Implementação do módulo de autenticação",
                    "project_id": 1,
                    "start_time": "2024-03-13T10:00:00Z",
                    "end_time": "2024-03-13T12:00:00Z"
                }
            ]
        }
    }
