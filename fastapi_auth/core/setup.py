from fastapi_auth.db.factory import get_repo
from fastapi_auth.services.auth_service import AuthService
from fastapi_auth.api.auth import router
from fastapi_auth.dependencies import auth

async def init_auth(app, config):
    repo = await get_repo(config)

    service = AuthService(repo, config.secret_key)

    auth.SECRET = config.secret_key

    app.state.auth = service
    app.include_router(router, prefix="/auth")