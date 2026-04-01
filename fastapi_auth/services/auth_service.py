from fastapi import HTTPException, status
from fastapi_auth.core.security import *

class AuthService:
    def __init__(self, repo, secret):
        self.repo = repo
        self.secret = secret

    async def register(self, username: str, password: str):
        existing_user = await self.repo.get_user(username)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists"
            )

        user = await self.repo.create_user(
            username,
            hash_password(password)
        )

        return {
            "message": "User registered successfully",
            "username": username
        }

    async def login(self, username: str, password: str):
        user = await self.repo.get_user(username)

        if not user or not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )

        access = create_token({"sub": username}, self.secret, 15, "access")
        refresh = create_token({"sub": username}, self.secret, 60*24, "refresh")

        await self.repo.save_refresh_token(refresh)

        return {
            "access": access,
            "refresh": refresh
        }

    async def refresh(self, token: str):
        try:
            data = decode_token(token, self.secret)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token"
            )

        if data.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token type (expected refresh token)"
            )

        if await self.repo.is_token_blacklisted(token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been revoked (logout)"
            )

        return {
            "access": create_token(
                {"sub": data["sub"]},
                self.secret,
                15,
                "access"
            )
        }

    async def logout(self, token: str):
        try:
            data = decode_token(token, self.secret)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token"
            )

        if data.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token type"
            )

        if await self.repo.is_token_blacklisted(token):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token already logged out"
            )

        await self.repo.blacklist_token(token)

        return {"message": "Logged out successfully"}