import functools
from fastapi import status
from fastapi.responses import JSONResponse
from src.helpers.helpers import formated_error
from src.helpers.jwt_helpers import validate_access_token
from src.configurations.config import access_control_list, prompts


def grant_access(fun):
    @functools.wraps(fun)
    def wrapper(*args, **kwargs):
        request = kwargs.get("request")
        token = validate_access_token(request=request)
        roles = token.get("role")
        operation = fun.__name__
        allowed_operations = []
        for role in roles:
            allowed_operations.extend(access_control_list.get(role))
        if operation in allowed_operations:
            return fun(*args, **kwargs)
        else:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content=formated_error(
                    error_code=500,
                    error_message=prompts.get("errors").get("FORBIDDEN_ERROR"),
                    status=prompts.get("errors").get("FORBIDDEN_STATUS"))
            )
    return wrapper
