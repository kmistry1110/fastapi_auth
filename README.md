# fastapi_auth
Auth APIs for FastAPI App

## Database support (db_type)
postgres \
mysql \
sqlite \
mongodb

## Available APIs
/register - to register user with username & password \
/login - login user  with username & password, returns refresh & access tokens \
/refresh - refresh token \
/logout - revoke refresh token \
/me - get user details

## How to use this  in your FastAPI App

### Step 1: How to initiate auth on startup
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
### Step 2: How to validate token for all your APIs
```
from fastapi import APIRouter, Depends
from fastapi_auth.dependencies.auth import get_current_user
router = APIRouter()

@router.get("/user")
async def me(user=Depends(get_current_user)):
    return user
```
