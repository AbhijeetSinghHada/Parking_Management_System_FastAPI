import logging
import functools
import jsonschema
from jsonschema import ValidationError, SchemaError
from fastapi import status
from fastapi.responses import JSONResponse
from src.configurations.config import prompts
from src.helpers.handle_errors import error_parser
from src.helpers.helpers import formated_error

logger = logging.getLogger(__name__)


def validate_request_data(request_data, schema):
    """Validate the request data according to schema"""

    try:
        jsonschema.validate(instance=request_data, schema=schema)

    except ValidationError as error:
        return error_parser(error)


def validate_body(schema):
    """Decorator to validate the request body"""
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            request_data = kwargs.get("request_data")
            print(request_data)
            validation_response = validate_request_data(
                request_data, schema)
            if validation_response:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content=formated_error(
                        400,
                        str(validation_response),
                        prompts.get("errors").get("BAD_REQUEST_ERROR")
                    )
                )
            return function(*args, **kwargs)

        return wrapper

    return decorator
