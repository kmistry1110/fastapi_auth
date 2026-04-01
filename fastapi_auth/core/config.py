from pydantic import BaseModel

class AuthConfig(BaseModel):
    secret_key: str
    db_url: str
    db_type: str  # postgres | mysql | sqlite | mongodb