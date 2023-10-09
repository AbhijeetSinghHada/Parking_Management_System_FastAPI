from datetime import timedelta
from fastapi import APIRouter, Body, Response
from src.controllers.login import Login
from src.schemas import user_schema
from src.models.database_helpers import DatabaseHelper
from src.models.database import Database
from src.helpers.jwt_helpers import create_access_token
from fastapi import APIRouter, Body, Request
from src.helpers.decorators import handle_errors, validate_body
import logging
logger = logging.getLogger(__name__)


router = APIRouter()

db = Database()
db_helper = DatabaseHelper(db)


router = APIRouter()


@router.post("/login")
@validate_body(user_schema)
@handle_errors
def login(response: Response, request_data=Body()):

    instance = Login(
        username=request_data.get("username"), password=request_data.get("password"), db=db)
    instance.authenticate()
    request_data = instance.fetch_user_roles()
    access_token = create_access_token(request_data, timedelta(minutes=60))
    response.set_cookie(key="access_token",
                        value=access_token, httponly=True)
    return {"message": "Login successful."}


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Logout successful."}
