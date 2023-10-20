user_schema = {
    "type": "object",
    "properties": {
        "username": {
            "type": "string",
            "pattern": r"^[A-Za-z0-9]+(?:[ _-][A-Za-z0-9]+)*$",
            "minLength": 3,
            "message": {
                "required": "username is a required property",
                "pattern": "username should contain only alphanumeric characters, spaces, hyphens and underscores",
                "minLength": "username should be atleast 3 characters long"
        }},
        "password": {
            "type": "string",
            "pattern": r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{5,}$",
            "message": {
                "required": "password is a required property",
                "pattern": "password should contain atleast one uppercase, one lowercase, one digit and should be atleast 5 characters long"
        }}
    },
    "required": ["username", "password"]
}
