from src.helpers.decorators import admin_only, handle_errors, operator_only, validate_body
from src.helpers.driver_program import ProgramDriver
from src.schemas import post_parking_space_schema, parking_space_schema
from src.models.database_helpers import DatabaseHelper
from src.models.database import Database
from fastapi import APIRouter, Body, Request
import logging
logger = logging.getLogger(__name__)

db = Database()
db_helper = DatabaseHelper(db)
program_driver = ProgramDriver(db)
router = APIRouter()


@router.get("/parkingspace")
@handle_errors
@operator_only
def get_parking_space(request: Request):

    parking_spaces = program_driver.check_parking_capacity()
    return parking_spaces


@router.put("/parkingspace")
@validate_body(parking_space_schema)
@handle_errors
@admin_only
def update_parking_space(request: Request, request_data=Body()):

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


@router.post("/parkingspace")
@validate_body(post_parking_space_schema)
@handle_errors
@admin_only
def add_new_parking(request: Request, request_data=Body()):

    if request_data.get("total_capacity") and request_data.get("charge"):
        program_driver.add_vehicle_category(
            request_data.get("slot_type"), request_data.get("total_capacity"), request_data.get("charge"))
    else:
        raise ValueError(
            "Please insert total_capacity and charge fields both.")
    return request_data
