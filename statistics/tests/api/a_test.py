import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_s(client, app):
    a = await client.get(url="/api/v1/analytics/project/list")
    assert a.status_code == status.HTTP_200_OK
