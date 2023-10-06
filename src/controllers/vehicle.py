from src.helpers import helpers
import logging

logger = logging.getLogger(__name__)


class Vehicle:
    def __init__(self, db_helpers):
        self.sql_queries = helpers.get_sql_queries()
        super().__init__()
        self.vehicle_number = None
        self.vehicle_type = None
        self.db_helpers = db_helpers

    def check_if_vehicle_exists(self, vehicle_number):
        logger.debug(
            "check_if_vehicle_exists called with params {}".format(vehicle_number))
        data = self.db_helpers.get_vehicle_data(vehicle_number=vehicle_number)
        if data:
            return data
        return None

    def add_vehicle(self, vehicle_number, vehicle_type):
        logger.debug("add_vehicle called with params {},{}".format(
            vehicle_number, vehicle_type))

        self.db_helpers.insert_vehicle(vehicle_number, vehicle_type)

    def add_vehicle_category(self, slot_type, total_capacity, parking_charge):
        self.db_helpers.add_vehicle_category(
            slot_type, total_capacity, parking_charge)
