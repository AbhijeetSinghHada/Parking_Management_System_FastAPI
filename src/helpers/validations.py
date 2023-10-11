import functools
import traceback
import logging
import jsonschema
from fastapi.responses import JSONResponse
from jsonschema import ValidationError
from fastapi import status
from src.configurations.config import prompts
from src.helpers.helpers import formated_error
logger = logging.getLogger(__name__)


def validate_request_data(request_data, schema):
    try:
        jsonschema.validate(instance=request_data, schema=schema)
    except ValidationError as error:
        return error.message.split('\n')[0]


def validate_body(schema):
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            try:
                request_data = kwargs.get("request_data")
                validation_response = validate_request_data(
                    request_data, schema)
                if validation_response:
                    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=formated_error(400, str(validation_response), prompts.get("errors").get("BAD_REQUEST_ERROR")))
                return function(*args, **kwargs)
            except Exception as error:
                logger.debug("Error Occurred: {} Method Error: {}".format(function.__name__,
                                                                          traceback.format_exc()))
                logger.error("Error Occurred: {} Method Error: {}".format(function.__name__,
                                                                          str(error)))
                return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=formated_error(500, str(error), prompts.get("errors").get("INTERNAL_SERVER_ERROR")))
        return wrapper
    return decorator
