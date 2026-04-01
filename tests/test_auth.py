import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from fastapi_async_auth_kit import init_auth, AuthConfig


@pytest.mark.asyncio
async def test_auth_flow():
    app = FastAPI()

    @app.on_event("startup")
    async def setup():
        await init_auth(
            app,
            AuthConfig(
                secret_key="test",
                db_url="sqlite+aiosqlite:///:memory:",
                db_type="sqlite"
            )
        )

    async with AsyncClient(app=app, base_url="http://test") as ac:

        # register
        r = await ac.post("/auth/register", json={
            "username": "test",
            "password": "123"
        })
        assert r.status_code == 200

        # login
        r = await ac.post("/auth/login", json={
            "username": "test",
            "password": "123"
        })
        data = r.json()

        assert "access" in data
        assert "refresh" in data

        refresh = data["refresh"]

        # refresh token
        r = await ac.post("/auth/refresh", json={"refresh": refresh})
        assert r.status_code == 200

        # logout
        r = await ac.post("/auth/logout", json={"refresh": refresh})
        assert r.status_code == 200

        # refresh again (should fail)
        r = await ac.post("/auth/refresh", json={"refresh": refresh})
        assert r.status_code != 200