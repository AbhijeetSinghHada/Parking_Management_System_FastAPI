import re
import jsonschema
from jsonschema import ValidationError

EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
USERNAME_REGEX = r"^[A-Za-z0-9]+(?:[ _-][A-Za-z0-9]+)*$"
PASSWORD_REGEX = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{5,}$"
VEHICLE_NUMBER_REGEX = r"^[A-Z]{2}\d{2}[A-Z]{2}\d{4}$"


def validate_vehicle_number(vehicle_number):
    if not re.match(VEHICLE_NUMBER_REGEX, vehicle_number):
        raise ValueError("Invalid Vehicle Number.")
    return True


def validate_integer_input(user_input):
    if not re.match(r'^[0-9]+$', str(user_input)):
        raise ValueError("Invalid Integer Input.")
    return True


def validate_string_input(user_input):
    if not re.match(r'^[A-Za-z]+$', user_input):
        raise ValueError("Invalid String Input.")
    return True


def validate_phone_number(phone_number):
    if not re.match(r'^\d{10}$', str(phone_number)):
        raise ValueError("Invalid Phone Number.")
    return True


def validate_email(email):
    if not re.fullmatch(EMAIL_REGEX, email):
        raise ValueError("Invalid Email Address.")
    return True


def validate_request_data(request_data, schema):
    try:
        jsonschema.validate(instance=request_data, schema=schema)
    except ValidationError as error:
        return error.message.split('\n')[0]
