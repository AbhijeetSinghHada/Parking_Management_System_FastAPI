import functools
import traceback
from fastapi import status
from fastapi.responses import JSONResponse
from src.helpers.errors import UnauthorizedError
from src.helpers.helpers import formated_error
from src.configurations.config import prompts
import logging
logger = logging.getLogger(__name__)


def handle_errors(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return_value = function(*args, **kwargs)
            return return_value

        except UnauthorizedError as error:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                                content=formated_error(401, str(error),  prompts.get("errors").get("UNAUTHORIZED_ERROR")))
        except LookupError as error:
            return JSONResponse(status_code=status.HTTP_409_CONFLICT,
                                content=formated_error(409, str(error),  prompts.get("errors").get("CONFLICT_ERROR")))
        except ValueError as error:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content=formated_error(400, str(error), prompts.get("errors").get("BAD_REQUEST_ERROR")))
        except Exception as error:
            logger.debug("Error Occurred: {} Method Error: {}".format(function.__name__,
                                                                      traceback.format_exc()))
            logger.error("Error Occurred: {} Method Error: {}".format(function.__name__,
                                                                      str(error)))
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                content=formated_error(500, str(error), prompts.get("errors").get("INTERNAL_SERVER_ERROR")),
                                )
    return wrapper
