from fastapi import APIRouter, Body, Request
from src.helpers.decorators import handle_errors, operator_only, validate_body
from src.helpers.driver_program import ProgramDriver
from src.schemas import vehicle_schema
from src.models.database_helpers import DatabaseHelper
from src.models.database import Database
import logging
logger = logging.getLogger(__name__)
db = Database()
db_helper = DatabaseHelper(db)
program_driver = ProgramDriver(db)

router = APIRouter()


@router.post("/vehicle")
@validate_body(vehicle_schema)
@handle_errors
@operator_only
def add_vehicle(request: Request, request_data=Body()):
    """Add a vehicle to the database"""
    parameters = (request_data.get("vehicle_number"),
                  request_data.get("vehicle_type"),
                  request_data.get("customer").get("customer_id"),
                  request_data.get("customer").get("name"),
                  request_data.get("customer").get("email_address"),
                  request_data.get("customer").get("phone_number"))
    data, response = program_driver.add_vehicle(*parameters)
    data["message"] = response
    return data
