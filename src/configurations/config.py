import json
from src.helpers.errors import AuthenticationError, UnauthorizedError, ConflictError

def load_configuration():
    """Load the configuration file and return the parameters"""
    
    with open("src/configurations/config.json", "r") as file:
        config = json.load(file)
        connection_params = config.get("CONNECTION_PARAMETERS")
        prompt_path = config.get("PROMPTS_PATH")
        sql_queries_path = config.get("SQL_QUERIES_PATH")
        errors_format = config.get("ERROR_FORMAT")
        access_controls_list = config.get("ACCESS_CONTROL_LIST")
        prompt = get_prompts(prompt_path)
        _sql_queries = get_sql_queries(sql_queries_path)

        return connection_params, prompt, _sql_queries, errors_format, access_controls_list


def get_prompts(prompts_path):
    with open(prompts_path, "r") as file:
        return json.load(file)


def get_sql_queries(sql_queries_path):
    with open(sql_queries_path, "r") as file:
        return json.load(file)


(connection_parameters,
 prompts, sql_queries,
 error_format, access_control_list) = load_configuration()

error_map = {
        UnauthorizedError: (401, "UNAUTHORIZED_ERROR"),
        ConflictError: (409, "CONFLICT_ERROR"),
        ValueError: (400, "BAD_REQUEST_ERROR"),
        AuthenticationError: (401, "AUTHENTICATION_ERROR"),
        Exception : (500, "INTERNAL_SERVER_ERROR")
    }