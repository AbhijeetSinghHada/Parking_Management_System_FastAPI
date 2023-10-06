from src.helpers.errors import ConflictError
from src.controllers.billing import Billing
from src.controllers.parking_space import ParkingSpace
from src.helpers.helpers import get_prompts, return_date_and_time
from src.models.database import Database
from src.models.database_helpers import DatabaseHelper
from src.controllers.slot import Slot
from src.controllers.vehicle import Vehicle
from src.helpers import validations
import logging

logger = logging.getLogger(__name__)
prompts = get_prompts()


class ProgramDriver:

    def __init__(self, db):
        self.db_helper = DatabaseHelper(db)

    def assign_slot(self, slot_number, vehicle_type, vehicle_number):

        validations.validate_integer_input(slot_number)
        validations.validate_string_input(vehicle_type)
        validations.validate_vehicle_number(vehicle_number)

        slot = Slot(self.db_helper)
        parking_space = ParkingSpace(self.db_helper)
        parking_space.check_if_vehicle_type_exists(vehicle_type)
        parking_space.check_if_slot_in_range(slot_number, vehicle_type)
        slot.check_if_slot_already_occupied(slot_number, vehicle_type)

        slots_data = self.db_helper.get_slots_data()

        for i in slots_data:
            if i[5] == vehicle_number:
                raise ConflictError("Vehicle has a Slot Already Assigend.")

        data = slot.check_if_vehicle_exists(vehicle_number)
        if not data:
            raise ValueError(
                "Vehicle do not exist in the database. Please Add First")

        fetched_vehicle_type = data[0][5]
        if vehicle_type != fetched_vehicle_type:
            raise ValueError(
                "Wrong slot type for vehicle! Choose the correct Type.")

        date, time = return_date_and_time()
        billing = Billing(self.db_helper)
        billing.insert_into_bill_table(vehicle_number, date, time)
        slot.assign_slot(slot_number, vehicle_number, vehicle_type)

    def get_slot_table_by_category(self, vehicle_type):

        validations.validate_string_input(vehicle_type)
        slot = Slot(self.db_helper)
        return slot.get_slot_data_by_slot_type(vehicle_type)

    def add_vehicle(self, vehicle_number, vehicle_type, customer_id, name, email_address, phone_number):

        validations.validate_vehicle_number(vehicle_number)
        validations.validate_string_input(vehicle_type)
        validations.validate_string_input(name)
        validations.validate_email(email_address)
        validations.validate_phone_number(phone_number)

        vehicle = Vehicle(self.db_helper)
        parking_space = ParkingSpace(self.db_helper)
        if vehicle.check_if_vehicle_exists(vehicle_number):
            raise LookupError("Vehicle Already Exists.")

        parking_space.check_if_vehicle_type_exists(vehicle_type)

        customer_data = self.db_helper.fetch_customer_data(
            customer_id, email_address, phone_number)
        if customer_data:
            customer_id = customer_data[0][0]
            self.db_helper.insert_vehicle_by_customer_id(
                customer_id, vehicle_number, vehicle_type)
            formatted_data = {"customer": {"customer_id": customer_data[0][0], "name": customer_data[0][1], "email_address": customer_data[0][2],
                              "phone_number": customer_data[0][3]}, "vehicle_number": vehicle_number,
                              "vehicle_type": vehicle_type}
            return formatted_data, "Vehicle Added Successfully. Customer Details Existed."

        customer_id = self.db_helper.insert_customer_details(
            name, email_address, phone_number)
        vehicle.add_vehicle(vehicle_number, vehicle_type)
        formatted_data = {"customer": {"customer_id": customer_id, "name": name, "email_address": email_address,
                              "phone_number": phone_number}, "vehicle_number": vehicle_number,
                              "vehicle_type": vehicle_type}
        return formatted_data, "Vehicle Added Successfully. Customer Details Added."

    def add_vehicle_category(self, slot_type, total_capacity, parking_charge):

        validations.validate_string_input(slot_type)
        validations.validate_integer_input(total_capacity)
        validations.validate_integer_input(parking_charge)

        vehicle = Vehicle(self.db_helper)
        existing_vehicles = self.db_helper.get_vehicle_category_data()
        for i in existing_vehicles:
            if slot_type.lower() == i[0].lower():
                raise ConflictError("Parking Space Type Already Exists.")
        if total_capacity < 0:
            raise ValueError("Total Capacity cannot be less than 0")
        if parking_charge < 0:
            raise ValueError("Parking Charge cannot be less than 0")
        vehicle.add_vehicle_category(slot_type, total_capacity, parking_charge)

    def check_parking_capacity(self):

        data = self.db_helper.get_vehicle_category_data()
        vehicle_data = [
            {"slot_type": i[0], "total_capacity": i[1], "charge": i[2]} for i in data]
        return vehicle_data

    def update_parking_space(self, new_capacity, parking_category):

        validations.validate_integer_input(new_capacity)
        validations.validate_string_input(parking_category)

        parking_space = ParkingSpace(self.db_helper)
        attributes = parking_space.get_parking_slot_attributes(
            parking_category)
        if not attributes:
            raise ValueError("No Parking Space Exists for this Category")
        if new_capacity < int(attributes[1]) and parking_space.are_vehicles_already_parked(parking_category,
                                                                                           new_capacity):
            raise ValueError("First Remove Vehicles From Parking Space Range")
        parking_space.update_parking_capacity(new_capacity, parking_category)

    def unassign_slot(self, vehicle_number):

        validations.validate_vehicle_number(vehicle_number)

        slots_data = self.db_helper.get_slots_data()
        for i in slots_data:
            if i[5] == vehicle_number:
                slot_number = i[0]
                vehicle_number = i[5]
                vehicle_type = i[2]
                slot_id = i[7]
                slot_charges = i[6]
                billing = Billing(self.db_helper)
                bill_id = i[4]
                billing.update_bill_table(bill_id, slot_charges)
                bill = billing.generate_bill(bill_id)
                slot = Slot(self.db_helper)
                slot.unassign_slot(slot_id)
                slot_data = {"slot_number": slot_number,
                             "vehicle_type": vehicle_type, "vehicle_number": vehicle_number}
                return slot_data, bill
        raise ValueError("Vehicle do not have any assigned slot.")

    def ban_slot(self, slot_number, vehicle_type):

        validations.validate_integer_input(slot_number)
        validations.validate_string_input(vehicle_type)

        slot = Slot(self.db_helper)
        parking_space = ParkingSpace(self.db_helper)
        parking_space.check_if_slot_in_range(slot_number, vehicle_type)
        slot.check_if_slot_already_occupied(slot_number, vehicle_type)
        slot.ban_slot(slot_number, vehicle_type)

    def unban_slot(self, slot_number, slot_type):

        validations.validate_integer_input(slot_number)
        validations.validate_string_input(slot_type)

        slot = Slot(self.db_helper)
        slot.unban_slot(slot_number, slot_type)

    def view_ban_slots(self):
        slot = Slot(self.db_helper)
        data = slot.view_ban_slots()
        return data

    def update_parking_charges(self, new_charges, parking_category):

        validations.validate_integer_input(new_charges)
        validations.validate_string_input(parking_category)

        parking_space = ParkingSpace(self.db_helper)
        parking_space.update_parking_charges(new_charges, parking_category)


if __name__ == '__main__':
    test_db = Database()
    ProgramDriver({"name": "Kittu", "user_id": 2, "roles": [1, 2]}, test_db)
