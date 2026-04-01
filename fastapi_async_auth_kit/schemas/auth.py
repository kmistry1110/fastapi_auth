from pydantic import BaseModel, Field, field_validator
import re


USERNAME_REGEX = r"^[a-zA-Z][a-zA-Z0-9_]{2,29}$"
PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$"


class RegisterRequest(BaseModel):
    username: str = Field(
        ...,
        description="3-30 chars, letters/numbers/_ only, must start with letter"
    )
    password: str = Field(
        ...,
        description="Min 8 chars, include uppercase, lowercase, number, special char"
    )

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        if not re.match(USERNAME_REGEX, v):
            raise ValueError(
                "Username must be 3-30 chars, start with letter, and contain only letters, numbers, underscores"
            )
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if not re.match(PASSWORD_REGEX, v):
            raise ValueError(
                "Password must be at least 8 characters long and include uppercase, lowercase, number, and special character"
            )
        return v


class LoginRequest(BaseModel):
    username: str
    password: str


class RefreshRequest(BaseModel):
    refresh: str


class TokenResponse(BaseModel):
    access: str
    refresh: str