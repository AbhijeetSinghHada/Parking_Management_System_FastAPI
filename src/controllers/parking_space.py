import logging
from src.models.database import db
from src.configurations.config import prompts, sql_queries
from src.helpers.logger import log
logger = logging.getLogger(__name__)


class ParkingSpace:
    vehicle_category_data = []

    @log(logger=logger)
    def add_parking_category(self, slot_type, total_capacity, parking_charge):

        db.update_item(
            sql_queries.get("add_vehicle_type"),
            (slot_type, total_capacity, parking_charge))
        self.__reset_vehicle_category_data()

    @log(logger=logger)
    def update_parking_capacity(self, new_capacity, parking_category):

        db.update_item(
            sql_queries.get("update_vehicle_capacity"), (new_capacity, parking_category))
        self.__reset_vehicle_category_data()

    @log(logger=logger)
    def update_parking_charges(self, new_charges, parking_category):

        db.update_item(
            sql_queries.get("update_vehicle_charges"), (new_charges, parking_category))
        self.__reset_vehicle_category_data()

    @log(logger=logger)
    def parking_space_details(self):

        data = self.__get_parking_space_details()
        vehicle_data = [
            {"slot_type": i[0], "total_capacity": i[1], "charge": i[2]} for i in data]
        return vehicle_data

    @log(logger=logger)
    def get_parking_category_details(self, parking_category):
        vehicle_category_data = self.__get_parking_space_details()
        parking_category_data = None
        for i in vehicle_category_data:
            if parking_category == i[0]:
                parking_category_data = i
        return parking_category_data

    @log(logger=logger)
    def is_slot_number_existing(self, slot_number, parking_category):
        parking_category_data = self.get_parking_category_details(
            parking_category)
        if slot_number > parking_category_data[1]:
            raise ValueError(prompts.get("SLOT_NUMBER_EXCEEDS_CAPACITY"))

    @log(logger=logger)
    def is_vehicle_type_existing(self, vehicle_type):
        vehicle_category_data = self.__get_parking_space_details()
        for i in vehicle_category_data:
            if vehicle_type == i[0]:
                return
        raise ValueError(prompts.get("VEHICLE_TYPE_NOT_FOUND"))

    @log(logger=logger)
    def get_parking_capacity(self, vehicle_type):
        try:
            self.vehicle_category_data = self.__get_parking_space_details()
            for category in self.vehicle_category_data:
                if category[0] == vehicle_type:
                    return category[1]
        except Exception as exc:
            raise ResourceWarning(prompts.get(
                "FETCH_PARKING_CAPACITY_ERROR")) from exc

    def __get_parking_space_details(self):
        try:
            if self.vehicle_category_data:
                return self.vehicle_category_data
            self.vehicle_category_data = db.get_multiple_items(
                sql_queries.get("vehicle_category_data"))
            return self.vehicle_category_data
        except Exception as exc:
            raise ResourceWarning(prompts.get(
                "FETCH_PARKING_SPACE_ERROR")) from exc

    @classmethod
    def __reset_vehicle_category_data(self):
        ParkingSpace.all_slots_data = []
