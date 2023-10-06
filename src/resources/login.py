from flask_jwt_extended import create_access_token
from src.helpers.validations import validate_request_data
from src.controllers.login import Login
from src.schemas import user_schema
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from src.models.database_helpers import DatabaseHelper
from src.models.database import Database

blp = Blueprint("login", __name__, description="Operations on login")


db = Database()
db_helper = DatabaseHelper(db)


@blp.route("/login")
class UserLogin(MethodView):
    def post(self):
        user_data = request.get_json()
        validation_response = validate_request_data(
            user_data, user_schema)
        if validation_response:
            return validation_response, 400
        try:
            instance = Login(
                username=user_data["username"], password=user_data["password"], db=db)
            instance.authenticate()
        except Exception:
            abort(401, message="Invalid credentials.")
        else:
            user_data = instance.fetch_user_roles()
            access_token = create_access_token(
                identity=user_data.get("user_id"), additional_claims=user_data)
            return {"access_token": access_token}, 200
