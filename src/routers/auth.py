from datetime import timedelta
from fastapi import APIRouter, Body
from src.controllers.login import Login
from src.helpers.jwt_helpers import create_access_token
from src.helpers.handle_errors import handle_errors
from src.helpers.validations import validate_body
from src.helpers.schemas.user_schema import user_schema


router = APIRouter()


@router.post("/login")
@handle_errors
@validate_body(user_schema)
def login(request_data=Body()):
    """Login to the application"""

    instance = Login(
        username=request_data.get("username"), password=request_data.get("password"))
    instance.authenticate()
    request_data = instance.fetch_user_roles()
    access_token = create_access_token(request_data, timedelta(seconds=3600))
    response_data = {
        "access_token": access_token,
        "token_type": "bearer"
    }
    return response_data
