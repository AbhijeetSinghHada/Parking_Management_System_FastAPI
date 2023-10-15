import functools
import traceback
import logging

from fastapi.responses import JSONResponse
from src.helpers.logger import log_debug
from src.helpers.helpers import formated_error
from src.configurations.config import prompts, error_map

logger = logging.getLogger(__name__)



def handle_errors(function):
    """Decorator to handle errors"""
    
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return_value = function(*args, **kwargs)
            return return_value

        except Exception as error:
            
            return get_error_response(error)

    return wrapper

def get_error_response(error):
    """Identify the error"""

    if type(error) in error_map:
        status_code, error_key = error_map[type(error)]
    else:
        log_debug(logger,
                "Error Occurred: {}".format(
                    traceback.format_exc()
                )
            )
        status_code, error_key = error_map[Exception]


    return JSONResponse(
        status_code=status_code,
        content=formated_error(
            status_code,
            str(error),
            prompts.get("errors").get(error_key)
        )
    )

