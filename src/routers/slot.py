from fastapi import APIRouter, Body, Request
from src.helpers.access_decorator import grant_access
from src.controllers.billing import Billing
from src.controllers.vehicle import Vehicle
from src.helpers.handle_errors import handle_errors
from src.helpers.validations import validate_body
from src.controllers.slot import Slot
from src.helpers.helpers import return_date_and_time
from src.helpers.schemas.slot_schemas import ban_slot_schema, slot_schema
from src.configurations.config import prompts

router = APIRouter()


@router.post("/slots/assign")
@handle_errors
@validate_body(slot_schema)
@grant_access
def occupy_slot(request: Request, request_data=Body()):
    """Park a vehicle"""
    slot = Slot()
    vehicle = Vehicle()
    billing = Billing()

    if not vehicle.check_if_vehicle_exists(request_data.get(
        "vehicle_number")):
        raise ValueError(prompts.get("VEHICLE_NOT_EXISTS"))

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
    """Get slot table showing slot status for every slot in the parking space"""

    slot = Slot()
    slot_table = slot.get_all_slot_status(slot_type)
    return slot_table


@router.delete("/slots/unassign")
@handle_errors
@grant_access
def unassign_slot(request: Request, vehicle_number):
    """Unpark a vehicle from a slot"""

    slot = Slot()
    billing = Billing()
    slot_details = slot.unassign_slot(vehicle_number)

    billing.update_bill_table(slot_details.get(
        "bill_id"), slot_details.get("slot_charges"))

    bill = billing.generate_bill(slot_details.get("bill_id"))
    return {"slot": slot_details, "bill": bill}


@router.post("/slots/ban")
@handle_errors
@grant_access
@validate_body(ban_slot_schema)
def ban_slot(request: Request, request_data=Body()):
    """Ban a slot, that no vehicle can be parked on it"""

    slot = Slot()
    slot.ban_slot(request_data.get("slot_number"),
                  request_data.get("slot_type"))
    return request_data


@router.post("/slots/unban")
@handle_errors
@grant_access
@validate_body(ban_slot_schema)
def unban_slot(request: Request, request_data=Body()):
    """Unban a slot"""

    slot = Slot()
    slot.unban_slot(request_data.get("slot_number"),
                    request_data.get("slot_type"))
    
    return request_data


@router.get("/slots/ban")
@handle_errors
@grant_access
def view_ban_slot(request: Request):
    """View all banned slots"""

    slot = Slot()
    slot_data = slot.view_ban_slots()
    return slot_data
