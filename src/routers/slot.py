from fastapi import APIRouter, Body, Request
from src.helpers.decorators import admin_only, handle_errors, operator_only, validate_body
from src.helpers.driver_program import ProgramDriver
from src.schemas import ban_slot_schema, slot_schema
from src.models.database_helpers import DatabaseHelper
from src.models.database import Database
import logging
logger = logging.getLogger(__name__)
router = APIRouter()

db = Database()
db_helper = DatabaseHelper(db)
program_driver = ProgramDriver(db)


@router.post("/slots")
@validate_body(slot_schema)
@handle_errors
@operator_only
def assign_slot(request: Request, request_data=Body()):
    """Assign a slot to a vehicle"""

    program_driver = ProgramDriver(db)
    program_driver.assign_slot(request_data.get("slot_number"), request_data.get(
        "vehicle_type"), request_data.get("vehicle_number"))
    return request_data


@router.get("/slots")
@handle_errors
@operator_only
def get_slot_table(request: Request, slot_type):

    slots = program_driver.get_slot_table_by_category(slot_type)
    return slots


@router.delete("/slots")
@handle_errors
@operator_only
def unpark_vehicle(request: Request, vehicle_number):

    slot_data, bill = program_driver.unassign_slot(vehicle_number)
    return {"slot": slot_data, "bill": bill}


@router.post("/slots/ban")
@validate_body(ban_slot_schema)
@handle_errors
@admin_only
def ban_slot(request: Request, request_data=Body()):
    program_driver.ban_slot(request_data.get("slot_number"),
                            request_data.get("vehicle_type"))
    return request_data


@router.delete("/slots/ban")
@validate_body(ban_slot_schema)
@handle_errors
@admin_only
def unban_slot(request: Request, request_data=Body()):

    program_driver.unban_slot(request_data.get("slot_number"),
                              request_data.get("vehicle_type"))
    logger.debug("Unbanned slot called with params: {}, {}".format(
        request_data.get("slot_number"), request_data.get("vehicle_type")))
    return request_data


@router.get("/slots/ban")
@handle_errors
@admin_only
def view_ban_slot(request: Request):

    slots = program_driver.view_ban_slots()
    return slots
