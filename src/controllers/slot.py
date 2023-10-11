import logging
from src.models.database import db
from src.controllers.parking_space import ParkingSpace
from src.helpers.errors import ConflictError
from src.configurations.config import prompts, sql_queries
from src.helpers.logger import log
logger = logging.getLogger(__name__)


class Slot(ParkingSpace):

    all_slots_data = []

    def __init__(self):
        self.slot_number = None

    @log(logger=logger)
    def get_all_slot_status(self, vehicle_type):

        slot_data = self.__get_slots_data()
        slot_type_capacity = self.get_parking_capacity(vehicle_type)
        if not slot_type_capacity:
            raise ValueError(prompts.get("INVALID_SLOT_TYPE"))
        occupied_slot_numbers = [x[0]
                                 for x in slot_data if x[2] == vehicle_type]
        slot_table = []

        for i in range(1, int(slot_type_capacity) + 1):
            if i in occupied_slot_numbers:
                slot_table.append({"slot_id": i, "status": "Occupied"})
                continue
            slot_table.append({"slot_id": i, "status": "Not Occupied"})
        return slot_table

    @log(logger=logger)
    def assign_slot(self, slot_number, vehicle_type, vehicle_number):

        self.is_vehicle_type_existing(vehicle_type)
        self.is_slot_number_existing(slot_number, vehicle_type)
        self.__is_slot_available(slot_number, vehicle_type)
        self.__is_already_parked(vehicle_number)

        db.update_item(sql_queries.get("insert_into_slot"),
                       (slot_number, vehicle_number, vehicle_type,))
        self.__reset_all_slot_data()

    @log(logger=logger)
    def unassign_slot(self, vehicle_number):
        slot_details = self.__get_slot_details_by_vehicle(vehicle_number)

        db.update_item(
            sql_queries.get("delete_parked_slot"), (slot_details.get("slot_id"),))
        self.__reset_all_slot_data()
        del slot_details["slot_id"]
        return slot_details

    @log(logger=logger)
    def ban_slot(self, slot_number, vehicle_type):
        self.is_slot_number_existing(slot_number, vehicle_type)
        self.__is_slot_available(slot_number, vehicle_type)

        db.update_item(sql_queries.get("ban_slot"),
                       (slot_number, vehicle_type))
        self.__reset_all_slot_data()
        return True

    @log(logger=logger)
    def view_ban_slots(self):
        logger.debug("view_ban_slots called")
        data = self.__get_slots_data()
        data = [{"slot_number": x[0], "vehicle_type": x[2]}
                for x in data if x[1] == -1]
        return data

    @log(logger=logger)
    def unban_slot(self, slot_number, slot_type):
        logger.debug("unban_slot called")
        db.update_item(
            sql_queries.get("unban_slot"), (slot_number, slot_type))
        self.__reset_all_slot_data()

    @classmethod
    def __get_slots_data(self):
        if self.all_slots_data:
            return self.all_slots_data
        Slot.all_slots_data = db.get_multiple_items(
            sql_queries.get("slot_data"))
        return self.all_slots_data

    def __is_already_parked(self, vehicle_number):
        slots_data = self.__get_slots_data()
        for slot in slots_data:
            if slot[5] == vehicle_number:
                raise ConflictError(prompts.get("VEHICLE_ALREADY_PARKED"))
        return False

    def __is_slot_available(self, slot_number, slot_type):
        slot_data = self.__get_slots_data()
        slot_data_by_type = [x[0] for x in slot_data if x[2] == slot_type]
        if slot_number in slot_data_by_type:
            raise LookupError(prompts.get("SLOT_OCCUPIED"))

    def __get_slot_details_by_vehicle(self, vehicle_number):
        slot_data = self.__get_slots_data()
        for slot in slot_data:
            if slot[5] == vehicle_number:
                slot_details = {}
                slot_details["slot_number"] = slot[0]
                slot_details["vehicle_number"] = slot[5]
                slot_details["vehicle_type"] = slot[2]
                slot_details["slot_id"] = slot[7]
                slot_details["slot_charges"] = slot[6]
                slot_details["bill_id"] = slot[4]
                return slot_details
        raise ValueError(prompts.get("VEHICLE_NOT_PARKED"))

    def is_space_occupied(self, parking_category, new_capacity):
        slot_data = self.__get_slots_data()
        for i in slot_data:
            if i[2] == parking_category and i[0] > new_capacity:
                return True
        return False

    @classmethod
    def __reset_all_slot_data(self):
        Slot.all_slots_data = []
