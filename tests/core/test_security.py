import pytest
from unittest.mock import AsyncMock
from fastapi import HTTPException
from app.core.security import get_api_key


@pytest.mark.asyncio
async def test_validate_api_key_success():

    api_key = "dev_api_key_super_secret"
    result = await get_api_key(api_key)
    assert result == api_key


@pytest.mark.asyncio
async def test_validate_api_key_invalid():
    api_key = "invalid_api_key"

    with pytest.raises(HTTPException) as exc:
        await get_api_key(api_key)
    assert exc.value.status_code == 403
    assert "Could not validate API key" == exc.value.detail


@pytest.mark.asyncio
async def test_validate_api_key_missing():
    api_key = None

    with pytest.raises(HTTPException) as exc:
        await get_api_key(api_key)
    assert exc.value.status_code == 403
    assert "Could not validate API key" == exc.value.detail
