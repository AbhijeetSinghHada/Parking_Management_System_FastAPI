import json

connection_parameters = None
error_format = None
access_control_list = None
sql_queries = None
prompts = None


def load_configuration():
    with open("src/configurations/config.json", "r") as fp:

        config = json.load(fp)
        connection_parameters = config.get("connection_parameters")
        prompts_path = config.get("prompts_path")
        sql_queries_path = config.get("sql_queries_path")
        error_format = config.get("error_format")
        access_control_list = config.get("access_control_list")
        prompts = get_prompts(prompts_path)
        sql_queries = get_sql_queries(sql_queries_path)

        return connection_parameters, prompts, sql_queries, error_format, access_control_list


def get_prompts(prompts_path):
    with open(prompts_path, "r") as fp:
        return json.load(fp)


def get_sql_queries(sql_queries_path):
    with open(sql_queries_path, "r") as fp:
        return json.load(fp)


connection_parameters, prompts, sql_queries, error_format, access_control_list = load_configuration()
