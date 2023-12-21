from fastapi import APIRouter, Body, Request
from src.controllers.slot import Slot
from src.helpers.errors import ConflictError
from src.helpers.validations import validate_body
from src.helpers.handle_errors import handle_errors
from src.helpers.access_decorator import grant_access
from src.controllers.parking_space import ParkingSpace
from src.configurations.config import prompts
from src.helpers.schemas.parking_space_schemas import (
    parking_space_schema_all_required, 
    parking_space_schema)


router = APIRouter()


@router.get("/parkingspace")
@handle_errors
@grant_access
def get_parking_space(request: Request):
    """Get parking space details"""
    
    parking_space = ParkingSpace()
    parking_space_data = parking_space.parking_space_details()
    return parking_space_data


@router.put("/parkingspace/update")
@handle_errors
@grant_access
@validate_body(parking_space_schema)
def update_parking_space(request: Request, request_data=Body()):
    """Update parking space details"""

    parking_space = ParkingSpace()
    slot = Slot()
    if request_data.get("total_capacity"):
        if slot.is_space_occupied(request_data.get("slot_type"),
                                  request_data.get("total_capacity")):
            raise ConflictError(prompts.get("SPACE_OCCUPIED"))

        parking_space.update_parking_capacity(
            request_data.get("total_capacity"), request_data.get("slot_type"))
    if request_data.get("charge"):
        parking_space.update_parking_charges(
            request_data.get("charge"), request_data.get("slot_type"))
    return request_data


@router.post("/parkingspace/add")
@handle_errors
@grant_access
@validate_body(parking_space_schema_all_required)
def add_new_parking_space(request: Request, request_data=Body()):
    """Add a new parking space"""

    parking_space = ParkingSpace()
    parking_space.add_parking_category(
        request_data.get("slot_type"), 
        request_data.get("total_capacity"), 
        request_data.get("charge"))
    
    return request_data
