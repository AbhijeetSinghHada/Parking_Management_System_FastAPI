from fastapi import APIRouter, Body, Request
from src.helpers.access_decorator import grant_access
from src.controllers.billing import Billing
from src.controllers.vehicle import Vehicle
from src.helpers.handle_errors import handle_errors
from src.helpers.validations import validate_body
from src.controllers.slot import Slot
from src.helpers.helpers import return_date_and_time
from src.schemas import ban_slot_schema, slot_schema
import logging
logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/slots")
@validate_body(slot_schema)
@handle_errors
@grant_access
def park_vehicle(request: Request, request_data=Body()):
    """Assign a slot to a vehicle"""
    slot = Slot()
    vehicle = Vehicle()
    billing = Billing()
    vehicle.check_if_vehicle_exists(request_data.get(
        "vehicle_type"))

    date, time = return_date_and_time()
    billing.insert_into_bill_table(request_data.get(
        "vehicle_number"), date, time)
    slot.assign_slot(request_data.get("slot_number"), request_data.get(
        "vehicle_type"), request_data.get("vehicle_number"))
    return request_data


@router.get("/slots")
@handle_errors
@grant_access
def get_slot_table(request: Request, slot_type):

    slot = Slot()
    slot_table = slot.get_all_slot_status(slot_type)
    return slot_table


@router.delete("/slots")
@handle_errors
@grant_access
def unpark_vehicle(request: Request, vehicle_number):

    slot = Slot()
    billing = Billing()
    slot_details = slot.unassign_slot(vehicle_number)

    billing.update_bill_table(slot_details.get(
        "bill_id"), slot_details.get("slot_charges"))

    bill = billing.generate_bill(slot_details.get("bill_id"))
    return {"slot": slot_details, "bill": bill}


@router.post("/slots/ban")
@validate_body(ban_slot_schema)
@handle_errors
@grant_access
def ban_slot(request: Request, request_data=Body()):
    slot = Slot()
    slot.ban_slot(request_data.get("slot_number"),
                  request_data.get("vehicle_type"))
    return request_data


@router.patch("/slots/ban")
@validate_body(ban_slot_schema)
@handle_errors
@grant_access
def unban_slot(request: Request, request_data=Body()):
    slot = Slot()
    slot.unban_slot(request_data.get("slot_number"),
                    request_data.get("vehicle_type"))
    logger.debug("Unbanned slot called with params: {}, {}".format(
        request_data.get("slot_number"), request_data.get("vehicle_type")))
    return request_data


@router.get("/slots/ban")
@handle_errors
@grant_access
def view_ban_slot(request: Request):
    slot = Slot()
    slot_data = slot.view_ban_slots()
    return slot_data
