import logging
from src.configurations.config import prompts, sql_queries
from src.controllers.parking_space import ParkingSpace
from src.models.database import db
from src.helpers.logger import log
logger = logging.getLogger(__name__)


class Vehicle:
    all_vehicles_data = []

    @log(logger=logger)
    def check_if_vehicle_exists(self, vehicle_number):
        data = self.__get_vehicle_data(vehicle_number=vehicle_number)
        for vehicle in data:
            if vehicle[4] == vehicle_number:
                return True
        return False

    @log(logger=logger)
    def add_vehicle(self, vehicle_number, vehicle_type, customer_id):
        parking_space = ParkingSpace()
        if self.check_if_vehicle_exists(vehicle_number):
            raise ValueError(prompts.get("VEHICLE_ALREADY_EXISTS"))
        parking_space.is_vehicle_type_existing(vehicle_type)

        self.__insert_vehicle(customer_id, vehicle_number, vehicle_type)
        Vehicle.all_vehicles_data = []
        return True

    @log(logger=logger)
    def __get_vehicle_data(self, vehicle_number='', customer_id='', email_address=''):
        try:
            if self.all_vehicles_data:
                return self.all_vehicles_data
            Vehicle.all_vehicles_data = db.get_multiple_items(sql_queries.get("fetch_vehicle_data"),
                                                              (vehicle_number, customer_id, email_address))
            return self.all_vehicles_data
        except Exception as exc:
            raise ResourceWarning(prompts.get(
                "CANNOT_FETCH_VEHICLE_DATA")) from exc

    @log(logger=logger)
    def __insert_vehicle(self, customer_id, vehicle_number, vehicle_type):
        try:
            db.update_item(
                sql_queries.get("insert_vehicle_by_customer_id"),
                (customer_id, vehicle_number, vehicle_type))
        except Exception as exc:
            raise ResourceWarning(prompts.get(
                "CANNOT_INSERT_VEHICLE_DATA")) from exc
