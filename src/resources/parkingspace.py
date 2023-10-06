import traceback
from flask_jwt_extended import jwt_required, get_jwt
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from src.helpers.validations import validate_request_data
from src.helpers.driver_program import ProgramDriver
from src.schemas import post_parking_space_schema, parking_space_schema
from src.models.database_helpers import DatabaseHelper
from src.models.database import Database
import logging
logger = logging.getLogger(__name__)

blp = Blueprint("parkingspace", __name__,
                description="Operations on Parking Space")


db = Database()
db_helper = DatabaseHelper(db)
program_driver = ProgramDriver(db)


@blp.route("/parkingspace")
class ParkingSpace(MethodView):

    @jwt_required()
    def get(self):
        jwt = get_jwt()
        role = jwt.get("role")
        if "Admin" not in role and "Operator" not in role:
            abort(403, message="Forbidden")

        try:
            parking_spaces = program_driver.check_parking_capacity()
            return parking_spaces
        except LookupError as error:
            abort(409, message=str(error))
        except ValueError as error:
            abort(400, message=str(error))
        except Exception as error:
            logger.debug("Error Occurred: ParkingSpace(MethodView) Method: get() Error: {}".format(
                traceback.format_exc()))
            logger.error("Error Occurred: ParkingSpace(MethodView) Method: get() Error: {}".format(
                str(error)))
            abort(500, message="An Error Occurred Internally in the Server")

    @jwt_required()
    def put(self):
        jwt = get_jwt()
        if "Admin" not in jwt.get("role"):
            abort(403, message="Forbidden")

        request_data = request.get_json()
        validation_response = validate_request_data(
            request_data, parking_space_schema)
        if validation_response:
            abort(400, message=validation_response)

        try:
            if request_data.get("total_capacity"):
                if request_data.get("total_capacity") < 0:
                    raise ValueError("Total Capacity cannot be less than 0")
                program_driver.update_parking_space(
                    request_data.get("total_capacity"), request_data.get("slot_type"))
            if request_data.get("charge"):
                if request_data.get("charge") < 0:
                    raise ValueError("Charge cannot be less than 0")
                program_driver.update_parking_charges(
                    request_data.get("charge"), request_data.get("slot_type"))
            return request_data
        except LookupError as error:
            abort(409, message=str(error))
        except ValueError as error:
            abort(400, message=str(error))
        except Exception as error:
            logger.debug("Error Occurred: ParkingSpace(MethodView) Method: put() Error: {}".format(
                traceback.format_exc()))
            logger.error("Error Occurred: ParkingSpace(MethodView) Method: put() Error: {}".format(
                str(error)))
            abort(500, message="An Error Occurred Internally in the Server")

    @jwt_required()
    def post(self):
        jwt = get_jwt()
        if "Admin" not in jwt.get("role"):
            abort(403, message="Forbidden")

        request_data = request.get_json()
        validation_response = validate_request_data(
            request_data, post_parking_space_schema)
        if validation_response:
            abort(400, message=validation_response)

        try:
            if request_data.get("total_capacity") and request_data.get("charge"):
                program_driver.add_vehicle_category(
                    request_data.get("slot_type"), request_data.get("total_capacity"), request_data.get("charge"))
            else:
                abort(
                    400, message="Please insert total_capacity and charge fields both.")
            return request_data

        except LookupError as error:
            abort(409, message=str(error))
        except ValueError as error:
            abort(400, message=str(error))
        except Exception as error:
            logger.debug("Error Occurred: ParkingSpace(MethodView) Method: post() Error: {}".format(
                traceback.format_exc()))
            logger.error("Error Occurred: ParkingSpace(MethodView) Method: post() Error: {}".format(
                str(error)))
            abort(500, message="An Error Occurred Internally in the Server")
