from .customer_schemas import customer_schema

vehicle_schema = {
    "type": "object",
    "properties": {
        "message": {"type": "string"},
        "vehicle_number": {
            "type": "string",
            "pattern": r"^[A-Z]{2}\d{2}[A-Z]{2}\d{4}$"},
        "vehicle_type": {"type": "string"},
        "customer": customer_schema
    },
    "required": ["vehicle_number", "vehicle_type", "customer"
                 ]
}