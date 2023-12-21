import logging
from fastapi import APIRouter, Body, Request
from src.controllers.parking_space import ParkingSpace
from src.controllers.vehicle import Vehicle
from src.controllers.customer import Customer
from src.helpers.access_decorator import grant_access
from src.helpers.handle_errors import handle_errors
from src.helpers.validations import validate_body
from src.configurations.config import prompts
from src.helpers.schemas.vehicle_schema import vehicle_schema
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/vehicle")
@handle_errors
@grant_access
@validate_body(vehicle_schema)
def add_vehicle(request: Request, request_data=Body()):
    """Add a new vehicle to the system"""

    customer = Customer()
    vehicle = Vehicle()
    parking = ParkingSpace()

    customer_data = customer.fetch_customer_data(
        request_data.get("customer").get("customer_id"),
        request_data.get("customer").get("email_address"),
        request_data.get("customer").get("phone_number")
    )

    if customer_data:
        customer_id = customer_data[0][0]
        request_data['customer'] = {
            "name" : customer_data[0][1],
            "email_address" : customer_data[0][2],
            "phone_number" : customer_data[0][3]
        }
        message = prompts.get("CUSTOMER_EXISTS_VEHICLE_ADDED")
    else:
        customer_id = customer.insert_customer_details(
            request_data.get("customer").get("name"),
            request_data.get("customer").get("email_address"),
            request_data.get("customer").get("phone_number")
        )
        message = prompts.get("CUSTOMER_AND_VEHICLE_ADDED")

    parking.is_vehicle_type_existing(request_data.get("vehicle_type"),)

    vehicle.add_vehicle(
        request_data.get("vehicle_number"),
        request_data.get("vehicle_type"),
        customer_id
    )

    request_data["message"] = message
    return request_data
