slot_schema = {
    "type": "object",
    "properties": {
        "slot_number": {
            "type": "integer",
            "minimum": 1},
        "vehicle_type": {"type": "string"},
        "vehicle_number": {
            "type": "string",
            "pattern": r"^[A-Z]{2}\d{2}[A-Z]{2}\d{4}$",
            "message": {
            "required": "Date of Birth is Required Property",
            "pattern": "Correct format of Date Of Birth is dd-mmm-yyyy"
        }
        }
    },
    "required": ["slot_number", "vehicle_type", "vehicle_number"]
}


ban_slot_schema = {
    "type": "object",
    "properties": {
        "slot_number": {"type": "integer",
                        "minimum": 1},
        "vehicle_type": {"type": "string"}
    },
    "required": ["slot_number", "vehicle_type"]
}