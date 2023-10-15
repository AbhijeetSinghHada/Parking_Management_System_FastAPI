user_schema = {
    "type": "object",
    "properties": {
        "username": {
            "type": "string",
            "pattern": r"^[A-Za-z0-9]+(?:[ _-][A-Za-z0-9]+)*$",
            "minLength": 3},
        "password": {
            "type": "string",
            "pattern": r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{5,}$"}
    },
    "required": ["username", "password"]
}
