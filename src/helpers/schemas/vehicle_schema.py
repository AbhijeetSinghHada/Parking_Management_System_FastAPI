from .customer_schemas import customer_schema

vehicle_schema = {
    "type": "object",
    "properties": {
        "vehicle_number": {
            "type": "string",
            "pattern": r"^[A-Z]{2}\d{2}[A-Z]{2}\d{4}$",
            "message": {
                "required": "vehicle_number is a required property",
                "pattern": "vehicle_number should be in the format of XX11XX1111"
        },
            },
        "vehicle_type": {"type": "string"},
        "customer": customer_schema
    },
    "required": ["vehicle_number", "vehicle_type", "customer"
                 ]
}