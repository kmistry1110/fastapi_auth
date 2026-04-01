from fastapi_auth.core.setup import init_auth
from fastapi_auth.core.config import AuthConfig
from fastapi_auth.dependencies.auth import get_current_user

__all__ = ["init_auth", "AuthConfig", "get_current_user"]