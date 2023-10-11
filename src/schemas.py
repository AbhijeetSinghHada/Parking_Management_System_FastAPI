
customer_schema = {
    "type": "object",
    "properties": {
        "customer_id": {
            "type": "integer",
            "minimum": 1
        },
        "name": {
            "type": "string",
            "pattern": "^[a-zA-Z ]+$",
            "minLength": 3},
        "email_address": {
            "type": "string",
            "pattern": "^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}"},
        "phone_number": {
            "type": "integer",
            "minimum": 1000000000,
            "maximum": 9999999999}
    },
    "required": ["name", "email_address", "phone_number"]
}

vehicle_schema = {
    "type": "object",
    "properties": {
        "message": {"type": "string"},
        "vehicle_number": {
            "type": "string",
            "pattern": "^[A-Z]{2}\d{2}[A-Z]{2}\d{4}$"},
        "vehicle_type": {"type": "string"},
        "customer": customer_schema
    },
    "required": ["vehicle_number", "vehicle_type", "customer"
                 ]
}


slot_status_schema = {
    "type": "object",
    "properties": {
        "slot_id": {
            "type": "integer",
            "minimum": 1
        },
        "status": {"type": "string"}
    }
}

list_slots_status_schema = {
    "type": "array",
    "items": slot_status_schema
}

slot_schema = {
    "type": "object",
    "properties": {
        "slot_number": {
            "type": "integer",
            "minimum": 1},
        "vehicle_type": {"type": "string"},
        "vehicle_number": {
            "type": "string",
            "pattern": "^[A-Z]{2}\d{2}[A-Z]{2}\d{4}$"}
    },
    "required": ["slot_number", "vehicle_type", "vehicle_number"]
}

bill_schema = {
    "type": "object",
    "properties": {
        "customer": customer_schema,
        "time_in": {"type": "string"},
        "time_out": {"type": "string"},
        "total_charges": {"type": "integer"}
    },
    "required": ["customer", "time_in", "time_out", "total_charges"]
}

remove_vehicle_from_slot_schema = {
    "type": "object",
    "properties": {
        "slot": slot_schema,
        "bill": bill_schema
    },
    "required": ["slot", "bill"]
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

list_banned_slots_schema = {
    "type": "array",
    "items": ban_slot_schema
}

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
post_parking_space_schema = {
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

list_parking_spaces_schema = {
    "type": "array",
    "items": parking_space_schema
}

user_schema = {
    "type": "object",
    "properties": {
        "username": {
            "type": "string",
            "pattern": "^[A-Za-z0-9]+(?:[ _-][A-Za-z0-9]+)*$",
            "minLength": 3},
        "password": {
            "type": "string",
            "pattern": "^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{5,}$"}
    },
    "required": ["username", "password"]
}
