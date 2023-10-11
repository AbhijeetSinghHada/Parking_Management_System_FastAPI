from fastapi import APIRouter, Body, Request
from src.controllers.customer import Customer
from src.controllers.vehicle import Vehicle
from src.helpers.access_decorator import grant_access
from src.helpers.handle_errors import handle_errors
from src.helpers.validations import validate_body
from src.schemas import vehicle_schema
import logging
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/vehicle")
@validate_body(vehicle_schema)
@handle_errors
@grant_access
def add_vehicle(request: Request, request_data=Body()):
    customer = Customer()
    vehicle = Vehicle()

    customer_data = customer.fetch_customer_data(
        request_data.get("customer").get("customer_id"),
        request_data.get("customer").get("email_address"),
        request_data.get("customer").get("phone_number")
    )

    if customer_data:
        customer_id = customer_data[0][0]
        message = "Vehicle Added Successfully. Customer Details Existed."
    else:
        customer_id = customer.insert_customer_details(
            request_data.get("customer").get("name"),
            request_data.get("customer").get("email_address"),
            request_data.get("customer").get("phone_number")
        )
        message = "Vehicle Added Successfully. Customer Details Added."

    vehicle.add_vehicle(
        request_data.get("vehicle_number"),
        request_data.get("vehicle_type"),
        customer_id
    )

    request_data["message"] = message
    return request_data
