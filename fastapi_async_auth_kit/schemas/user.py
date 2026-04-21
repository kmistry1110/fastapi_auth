from pydantic import BaseModel


class UserModel(BaseModel):
    id: str | None = None
    username: str
    password: str