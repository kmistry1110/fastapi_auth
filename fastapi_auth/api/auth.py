from fastapi import APIRouter, Request, Depends
from fastapi_auth.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    RefreshRequest,
    TokenResponse
)
from fastapi_auth.dependencies.auth import get_current_user

router = APIRouter()


@router.post("/register")
async def register(req: Request, data: RegisterRequest):
    return await req.app.state.auth.register(data.username, data.password)


@router.post("/login", response_model=TokenResponse)
async def login(req: Request, data: LoginRequest):
    return await req.app.state.auth.login(data.username, data.password)


@router.post("/refresh")
async def refresh(req: Request, data: RefreshRequest):
    return await req.app.state.auth.refresh(data.refresh)


@router.post("/logout")
async def logout(req: Request, data: RefreshRequest):
    return await req.app.state.auth.logout(data.refresh)

@router.get("/me")
async def me(user=Depends(get_current_user)):
    return user