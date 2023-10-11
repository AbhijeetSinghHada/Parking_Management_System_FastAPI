from src.helpers.handle_errors import handle_errors
from src.helpers.validations import validate_body
from src.helpers.access_decorator import grant_access
from src.helpers.errors import ConflictError
from src.schemas import post_parking_space_schema, parking_space_schema
from src.controllers.parking_space import ParkingSpace
from src.controllers.slot import Slot
from fastapi import APIRouter, Body, Request
import logging
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/parkingspace")
@handle_errors
@grant_access
def get_parking_space(request: Request):
    parking_space = ParkingSpace()
    parking_space_data = parking_space.parking_space_details()
    return parking_space_data


@router.put("/parkingspace")
@validate_body(parking_space_schema)
@handle_errors
@grant_access
def update_parking_space(request: Request, request_data=Body()):

    parking_space = ParkingSpace()
    slot = Slot()
    if request_data.get("total_capacity"):
        if slot.is_space_occupied(request_data.get("slot_type"),
                                  request_data.get("total_capacity")):
            raise ConflictError("Cannot reduce capacity. Space is occupied.")

        parking_space.update_parking_capacity(
            request_data.get("total_capacity"), request_data.get("slot_type"))
    if request_data.get("charge"):
        parking_space.update_parking_charges(
            request_data.get("charge"), request_data.get("slot_type"))
    return request_data


@router.post("/parkingspace")
@validate_body(post_parking_space_schema)
@handle_errors
@grant_access
def add_new_parking_space(request: Request, request_data=Body()):

    parking_space = ParkingSpace()
    parking_space.add_parking_category(
        request_data.get("slot_type"), request_data.get("total_capacity"), request_data.get("charge"))
    return request_data
