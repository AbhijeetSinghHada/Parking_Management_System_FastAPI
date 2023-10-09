from src.controllers.slot import Slot
from src.helpers import helpers
import logging

logger = logging.getLogger(__name__)
prompts = helpers.get_prompts()


class ParkingSpace(Slot):
    def __init__(self, db_helper):
        self.db_helper = db_helper

    def update_parking_capacity(self, new_capacity, parking_category):
        logger.debug("update_parking_space called, params - vehicle type : {}, new_capacity : {} ".format(
            parking_category, new_capacity))
        self.db_helper.update_parking_capacity(new_capacity, parking_category)

    def update_parking_charges(self, new_charges, parking_category):

        self.db_helper.update_charges(new_charges, parking_category)

    def get_parking_category_details(self, parking_category):
        vehicle_category_data = self.db_helper.get_vehicle_category_data()
        parking_category_data = None
        for i in vehicle_category_data:
            if parking_category == i[0]:
                parking_category_data = i
        return parking_category_data

    def is_space_occupied(self, parking_category, new_capacity):
        slot_data = self.db_helper.get_slots_data()
        for i in slot_data:
            if i[2] == parking_category and i[0] > new_capacity:
                return True
        return False

    def is_valid_slot(self, slot_number, parking_category): # shift
        parking_category_data = self.get_parking_category_details(
            parking_category)
        if slot_number > parking_category_data[1]:
            raise ValueError("Slot Number Exceeds the Total Capacity")

    def is_valid_vehicle_type(self, vehicle_type): # shift
        vehicle_category_data = self.db_helper.get_vehicle_category_data()
        for i in vehicle_category_data:
            if vehicle_type == i[0]:
                return
        raise ValueError("Vehicle Type Does Not Exist")
