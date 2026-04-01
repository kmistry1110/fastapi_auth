# fastapi_auth
Auth APIs for FastApi App

# Database support (db_type)
postgres
mysql
sqlite
mongodb

## How to use it in your FastAPI App

```
from fastapi import FastAPI
from fastapi_auth import init_auth, AuthConfig

app = FastAPI()

@app.on_event("startup")
async def startup():
    await init_auth(
        app,
        AuthConfig(
            secret_key="secret",
            db_url="postgresql+asyncpg://user:pass@localhost/db",
            db_type="postgres"
        )
    )
```
