parking_space_schema = {
    "type": "object",
    "properties": {
        "slot_type": {"type": "string"},
        "total_capacity": {"type": "integer",
                           "minimum": 1},
        "charge": {
            "type": "integer",
            "minimum": 1}
    },
    "required": ["slot_type"]
}

parking_space_schema_all_required = {
    "type": "object",
    "properties": {
        "slot_type": {"type": "string"},
        "total_capacity": {
            "type": "integer",
            "minimum": 1},
        "charge": {
            "type": "integer",
            "minimum": 1}
    },
    "required": ["slot_type", "total_capacity", "charge"]
}
