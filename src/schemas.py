
customer_schema = {
    "type" : "object",
    "properties" : {
        "customer_id" : {"type" : "integer"},
        "name" : {"type" : "string"},
        "email_address" : {"type" : "string"},
        "phone_number" : {"type" : "integer"}
    },
    "required" : ["name", "email_address", "phone_number"]
}

vehicle_schema = {
    "type" : "object",
    "properties" : {
        "message" : {"type" : "string"},
        "vehicle_number" : {"type" : "string"},
        "vehicle_type" : {"type" : "string"},
        "customer" : customer_schema
    },
    "required" : ["vehicle_number", "vehicle_type", "customer"
                  ]
}


slot_status_schema = {
    "type" : "object",
    "properties" : {
        "slot_id" : {"type" : "string"},
        "status" : {"type" : "string"}
    }
}

list_slots_status_schema = {
    "type" : "array",
    "items" : slot_status_schema
}

slot_schema = {
    "type" : "object",
    "properties" : {
        "slot_number" : {"type" : "integer"},
        "vehicle_type" : {"type" : "string"},
        "vehicle_number" : {"type" : "string"}
    },
    "required" : ["slot_number", "vehicle_type", "vehicle_number"]
}

bill_schema = {
    "type" : "object",
    "properties" : {
        "customer" : customer_schema,
        "time_in" : {"type" : "string"},
        "time_out" : {"type" : "string"},
        "total_charges" : {"type" : "integer"}
    },
    "required" : ["customer", "time_in", "time_out", "total_charges"]
}

remove_vehicle_from_slot_schema = {
    "type" : "object",
    "properties" : {
        "slot" : slot_schema,
        "bill" : bill_schema
    },
    "required" : ["slot", "bill"]
}

ban_slot_schema = {
    "type" : "object",
    "properties" : {
        "slot_number" : {"type" : "integer"},
        "vehicle_type" : {"type" : "string"}
    },
    "required" : ["slot_number", "vehicle_type"]
}

list_banned_slots_schema = {
    "type" : "array",
    "items" : ban_slot_schema
}

parking_space_schema = {
    "type" : "object",
    "properties" : {
        "slot_type" : {"type" : "string"},
        "total_capacity" : {"type" : "integer"},
        "charge" : {"type" : "integer"}
    },
    "required" : ["slot_type"]
}
post_parking_space_schema = {
    "type" : "object",
    "properties" : {
        "slot_type" : {"type" : "string"},
        "total_capacity" : {"type" : "integer"},
        "charge" : {"type" : "integer"}
    },
    "required" : ["slot_type", "total_capacity", "charge"]
}

list_parking_spaces_schema = {
    "type" : "array",
    "items" : parking_space_schema
}

user_schema = {
    "type" : "object",
    "properties" : {
        "username" : {"type" : "string"},
        "password" : {"type" : "string"}
    },
    "required" : ["username", "password"]
}
