import traceback
from flask_jwt_extended import jwt_required, get_jwt
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import request
from src.helpers.validations import validate_request_data
from src.helpers.driver_program import ProgramDriver
from src.schemas import vehicle_schema
from src.models.database_helpers import DatabaseHelper
from src.models.database import Database
import logging
logger = logging.getLogger(__name__)

blp = Blueprint("vehicle", __name__, description="Operations on Vehicles")


db = Database()
db_helper = DatabaseHelper(db)
program_driver = ProgramDriver(db)


@blp.route("/vehicle")
class Vehicle(MethodView):

    @jwt_required()
    def post(self):

        jwt = get_jwt()
        role = jwt.get("role")
        if "Admin" not in role and "Operator" not in role:
            abort(403, message="Forbidden.")

        request_data = request.get_json()

        validation_response = validate_request_data(
            request_data, vehicle_schema)
        if validation_response:
            abort(400, message=validation_response)

        parameters = (request_data.get("vehicle_number"), 
                      request_data.get("vehicle_type"),
                      request_data.get("customer").get("customer_id"), 
                      request_data.get("customer").get("name"),
                      request_data.get("customer").get("email_address"), 
                      request_data.get("customer").get("phone_number"))
        try:
            data, response = program_driver.add_vehicle(*parameters)
            data["message"] = response
            return data
        except LookupError as error:
            abort(409, message=str(error))
        except ValueError as error:
            abort(400, message=str(error))
        except Exception as error:
            logger.debug("Error Occurred: Vehicle(MethodView) Method: post() Traceback: {}".format(
                traceback.format_exc()))
            logger.error("Error Occurred: Vehicle(MethodView) Method: post() Error: {}".format(
                str(error)))
            abort(500, message="An Error Occurred Internally in the Server")
        
