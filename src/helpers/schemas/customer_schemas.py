
customer_schema = {
    "type": "object",
    "properties": {
        "customer_id": {
            "type": "integer",
            "minimum": 1
        },
        "name": {
            "type": "string",
            "pattern": r"^[a-zA-Z ]+$",
            "minLength": 3},
        "email_address": {
            "type": "string",
            "pattern": r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}"},
            
        "phone_number": {
            "type": "integer",
            "minimum": 1000000000,
            "maximum": 9999999999}
    },
    "required": ["name", "email_address", "phone_number"]
}
