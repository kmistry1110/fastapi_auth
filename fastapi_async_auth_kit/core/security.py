from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from jose import jwt
from datetime import datetime, timedelta

ph = PasswordHasher()

ALGO = "HS256"


def hash_password(password: str) -> str:
    return ph.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    try:
        ph.verify(hashed, password)
        return True
    except VerifyMismatchError:
        return False


def create_token(data, secret, minutes, ttype):
    payload = data.copy()
    payload.update({
        "exp": datetime.utcnow() + timedelta(minutes=minutes),
        "type": ttype
    })
    return jwt.encode(payload, secret, algorithm=ALGO)


def decode_token(token, secret):
    return jwt.decode(token, secret, algorithms=[ALGO])