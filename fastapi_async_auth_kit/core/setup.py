from fastapi_async_auth_kit.db.factory import get_repo
from fastapi_async_auth_kit.services.auth_service import AuthService
from fastapi_async_auth_kit.api.auth import router
from fastapi_async_auth_kit.dependencies import auth

async def init_auth(app, config):
    repo = await get_repo(config)

    service = AuthService(repo, config.secret_key)

    auth.SECRET = config.secret_key

    app.state.auth = service
    app.include_router(router, prefix="/auth")