import os
from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

os.environ["ENV_STATE"] = "test"

from storeapi.database import database  # noqa: E402
from storeapi.main import app  # noqa: E402


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture()
def client() -> Generator:
    yield TestClient(app)


@pytest.fixture(autouse=True)
async def db() -> AsyncGenerator:
    await database.connect()
    yield
    await database.disconnect()


@pytest.fixture()
async def async_client(client) -> AsyncGenerator:
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        yield ac


@pytest.fixture()
async def registed_user(async_client: AsyncClient) -> dict:
    user_details = {"email": "test@example.net", "password": "123"}
    await async_client.post("/register", json=user_details)
    return user_details
