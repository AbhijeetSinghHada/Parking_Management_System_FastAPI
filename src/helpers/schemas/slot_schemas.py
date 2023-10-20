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
                "required": "vehicle_number is a required property",
                "pattern": "vehicle_number should be in the format of XX11XX1111"
        }
        },
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