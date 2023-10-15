from typing import Optional
from datetime import datetime, timedelta
import os
import jwt
from environs import Env
from fastapi import Request
from src.helpers.errors import UnauthorizedError
from src.configurations.config import prompts

env = Env()
env.read_env(path="src/.env")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def validate_access_token(request: Request):
    """Validate the access token"""

    token = request.headers.get("Authorization").split(" ")[1]
    if not token:
        raise UnauthorizedError("Token Not Found")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError as exc:
        raise UnauthorizedError(prompts.get(
            "errors").get("EXPIRED_TOKEN_ERROR")) from exc
    except jwt.InvalidTokenError as exc:
        raise UnauthorizedError(prompts.get(
            "errors").get("INVALID_TOKEN_ERROR")) from exc
    return payload


def create_access_token(user_data: dict,
                        expires_delta: Optional[timedelta] = None):
    """Create an access token using the user data and the expiry time
    Args:
        user_data (dict): The user data
        expires_delta (Optional[timedelta], optional): The expiry time. Defaults to None.
    Returns: access token for the user"""

    encode = {"sub": user_data.get("user_id"), "name": user_data.get(
        "name"), "role": user_data.get("role")}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
