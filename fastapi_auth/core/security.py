from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

pwd = CryptContext(schemes=["argon2"], deprecated="auto")

ALGO = "HS256"


def hash_password(password: str) -> str:
    return pwd.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    valid = pwd.verify(password, hashed)

    if valid and pwd.needs_update(hashed):
        new_hash = pwd.hash(password)

    return valid


def create_token(data, secret, minutes, ttype):
    payload = data.copy()
    payload.update({
        "exp": datetime.utcnow() + timedelta(minutes=minutes),
        "type": ttype
    })
    return jwt.encode(payload, secret, algorithm=ALGO)


def decode_token(token, secret):
    return jwt.decode(token, secret, algorithms=[ALGO])