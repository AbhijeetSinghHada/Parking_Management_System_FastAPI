from datetime import datetime, timedelta
import os
from typing import Optional
from environs import Env
from fastapi import Request
import jwt
from src.configurations.config import prompts

from src.helpers.errors import UnauthorizedError
env = Env()
env.read_env(path="src/.env")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def validate_access_token(request: Request):
    token = request.headers.get("Authorization").split(" ")[1]
    if not token:
        raise UnauthorizedError("Token Not Found")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise UnauthorizedError(prompts.get(
            "errors").get("EXPIRED_TOKEN_ERROR"))
    except jwt.InvalidTokenError:
        raise UnauthorizedError(prompts.get(
            "errors").get("INVALID_TOKEN_ERROR"))
    return payload


def create_access_token(user_data: dict,
                        expires_delta: Optional[timedelta] = None):

    encode = {"sub": user_data.get("user_id"), "name": user_data.get(
        "name"), "role": user_data.get("role")}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
