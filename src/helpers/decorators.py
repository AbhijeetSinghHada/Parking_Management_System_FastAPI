
import functools
import traceback
from fastapi import status
from fastapi.responses import JSONResponse
from src.helpers.errors import UnauthorizedError
from src.helpers.helpers import formated_error
from src.helpers.jwt_helpers import validate_access_token
from src.helpers.validations import validate_request_data
import logging
logger = logging.getLogger(__name__)


def operator_only(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        request = kwargs.get("request")
        access_token = validate_access_token(request)
        role = access_token.get("role")
        if "Operator" not in role:
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=formated_error(403, "Your role do not have required permissions.", "Access Denied"))
        return function(*args, **kwargs)
    return wrapper


def admin_only(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        request = kwargs.get("request")
        access_token = validate_access_token(request)
        role = access_token.get("role")
        if "Admin" not in role:
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=formated_error(403, "Your role do not have required permissions.", "Access Denied"))
        return function(*args, **kwargs)
    return wrapper


def validate_body(schema):
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            try:
                request_data = kwargs.get("request_data")
                validation_response = validate_request_data(
                    request_data, schema)
                if validation_response:
                    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=formated_error(400, str(validation_response), "Bad Request"))
                return function(*args, **kwargs)
            except Exception as error:
                logger.debug("Error Occurred: {} Method Error: {}".format(function.__name__,
                                                                          traceback.format_exc()))
                logger.error("Error Occurred: {} Method Error: {}".format(function.__name__,
                                                                          str(error)))
                return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=formated_error(500, str(error), "An Error Occurred Internally in the Server"))
        return wrapper
    return decorator


def handle_errors(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return_value = function(*args, **kwargs)
            return return_value

        except UnauthorizedError as error:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=formated_error(401, str(error), "Unauthorized"))
        except LookupError as error:
            return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=formated_error(409, str(error), "Conflict in the Database"))
        except ValueError as error:
            logger.debug("Error Occurred: {} Method Error: {}".format(function.__name__,
                                                                      traceback.format_exc()))
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=formated_error(400, str(error), "Bad Request"))
        except Exception as error:
            logger.debug("Error Occurred: {} Method Error: {}".format(function.__name__,
                                                                      traceback.format_exc()))
            logger.error("Error Occurred: {} Method Error: {}".format(function.__name__,
                                                                      str(error)))
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=formated_error(500, str(error), "An Error Occurred Internally in the Server"))
    return wrapper
