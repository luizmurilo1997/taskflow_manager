from fastapi import HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader
from app.core.config import settings

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=True)


async def get_api_key(api_key_header: str = Security(API_KEY_HEADER)):
    """
    Validate the API Key provided in the request header.
    This function is used as a security dependency in FastAPI routes.

    Args:
        api_key_header: The API key from the request header

    Returns:
        str: The validated API key

    Raises:
        HTTPException: 403 Forbidden if the API key is invalid
    """
    if api_key_header == "dev_api_key_super_secret":
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate API key"
    )
