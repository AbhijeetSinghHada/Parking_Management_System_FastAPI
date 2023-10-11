from datetime import timedelta
from fastapi import APIRouter, Body, Response
from src.controllers.login import Login
from src.models.database import Database
from src.helpers.jwt_helpers import create_access_token
from src.helpers.handle_errors import handle_errors
from src.helpers.validations import validate_body
from src.schemas import user_schema



router = APIRouter()

db = Database()


router = APIRouter()


@router.post("/login")
@validate_body(user_schema)
@handle_errors
def login(response: Response, request_data=Body()):

    instance = Login(
        username=request_data.get("username"), password=request_data.get("password"))
    instance.authenticate()
    request_data = instance.fetch_user_roles()
    access_token = create_access_token(request_data, timedelta(minutes=60))
    response_data = {
        "access_token": access_token,
        "token_type": "bearer"
    }
    return response_data
