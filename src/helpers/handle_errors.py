import functools
import traceback
from fastapi.responses import JSONResponse
from src.helpers.logger import log_debug, get_logger
from src.helpers.helpers import formated_error
from src.configurations.config import prompts, error_map
from src.models.database import Database

logger = get_logger(__name__)



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
        status_code, error_key = error_map[Exception]
    log_debug(logger,
                "Error Occurred: {}".format(
                    traceback.format_exc()
                )
            )


    return JSONResponse(
        status_code=status_code,
        content=formated_error(
            status_code,
            str(error),
            prompts.get("errors").get(error_key)
        )
    )


def error_parser(error):
    try:
        message = error.schema.get("message").get(error.validator)
        return message
    except Exception as e:
        return error.message.split("\n")[0]
    

def handle_db_errors(function):
    """Decorator to handle database errors"""
    
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return_value = function(*args, **kwargs)
            return return_value

        except Exception as error:
            Database.reset()
            raise error

    return wrapper