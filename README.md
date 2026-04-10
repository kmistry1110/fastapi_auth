# FastAPI Auth 🔐

Production-ready authentication system for FastAPI with async support, JWT, refresh tokens, and pluggable database backends.

---

## 🚀 Features

* ⚡ Fully async (no blocking I/O)
* 🔐 JWT authentication (access + refresh tokens)
* 🔁 Refresh token flow
* 🚪 Logout with token blacklist
* 🧱 Multi-database support:

  * PostgreSQL (asyncpg)
  * MySQL (aiomysql)
  * SQLite (aiosqlite)
  * MongoDB (motor)
* 🧠 Dependency-based auth (FastAPI native)
* 📦 Plug-and-play integration
* 🛡️ Password hashing with Argon2 (modern standard)
* 📄 Clean OpenAPI (Swagger) docs with Pydantic schemas

---

## 📦 Installation

```bash
pip install "fastapi-async-auth-kit[<db>]"
```

### With database support

```bash
pip install "fastapi-async-auth-kit[postgres]"
pip install "fastapi-async-auth-kit[mysql]"
pip install "fastapi-async-auth-kit[mongodb]"
pip install "fastapi-async-auth-kit[sqlite]"
```

---

## ⚙️ Quick Start

### Step 1: How to initiate auth on startup
```python
from fastapi import FastAPI
from fastapi_async_auth_kit import init_auth, AuthConfig

app = FastAPI()

@app.on_event("startup")
async def startup():
    await init_auth(
        app,
        AuthConfig(
            secret_key="your-secret",
            db_url="postgresql+asyncpg://user:pass@localhost/db",
            db_type="postgres"
        )
    )
```

### Step 2: How to validate token for all your FastAPIs
```python
from fastapi import APIRouter, Depends
from fastapi_async_auth_kit.dependencies.auth import get_current_user
router = APIRouter()

@router.get("/user")
async def me(user=Depends(get_current_user)):
    return user
```


---

## 🔐 Available Endpoints

| Endpoint            | Description             |
| ------------------- | ----------------------- |
| POST /auth/register | Register new user       |
| POST /auth/login    | Login and get tokens    |
| POST /auth/refresh  | Refresh access token    |
| POST /auth/logout   | Logout and revoke token |
| GET /auth/me        | Get current user        |

![Swagger UI](https://raw.githubusercontent.com/kmistry1110/fastapi_auth/refs/heads/main/docs/image.png)
---

## 🧪 Example

### Login

```json
POST /auth/login

{
  "username": "john",
  "password": "Strong@123"
}
```

### Response

```json
{
  "access": "jwt_token",
  "refresh": "refresh_token"
}
```

---

## 🧠 Architecture

```
FastAPI App
   ↓
Auth Service
   ↓
Repository Layer
   ↓
Database (Async)
```

---

## 🛡️ Security

* Argon2 password hashing
* JWT token expiration
* Refresh token blacklist
* No sensitive data exposure
* Clean error handling

---

## 🧩 Extensibility

* Add RBAC (roles & permissions)
* Plug custom user models
* Add OAuth providers (Google, GitHub)
* Integrate Redis for token storage

---

## 🛠 Tech Stack

* FastAPI
* SQLAlchemy (async)
* Pydantic
* python-jose (JWT)
* Argon2 (password hashing)

---

## 📌 Roadmap

* [ ] RBAC support
* [ ] Redis token blacklist
* [ ] OAuth integration
* [ ] Rate limiting
* [ ] Email verification

---

## 🤝 Contributing

Pull requests are welcome. For major changes, open an issue first.

Source Code: https://github.com/kmistry1110/fastapi_auth

---

## 📄 License

MIT License
