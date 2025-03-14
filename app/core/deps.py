from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import get_api_key
from app.repositories.client_repository import ClientRepository


async def get_current_client(
    api_key: str = Depends(get_api_key),
    db: AsyncSession = Depends(get_db)
):
    """
    Dependency for API Key validation.
    This function is used as a FastAPI dependency to ensure
    that all protected endpoints have a valid API Key.

    Args:
        api_key: The API key from the request header (validated by get_api_key)
        db: Database session for potential future use

    Returns:
        bool: True if the API Key is valid

    Raises:
        HTTPException: If the API Key is invalid (handled by get_api_key)
    """
    return True
