import logging
from src.models.database import db
from src.configurations.config import prompts, sql_queries
logger = logging.getLogger(__name__)


class Vehicle:


    def add_vehicle(self, vehicle_number, vehicle_type, customer_id):
        """Add a new vehicle to the database
        Args:
            vehicle_number (str): The vehicle number of the vehicle to be added
            vehicle_type (str): The vehicle type of the vehicle to be added
            customer_id (int): The customer id of the customer to whom the vehicle belongs
        Returns: True if the vehicle is added"""

        if self.check_if_vehicle_exists(vehicle_number):
            raise ValueError(prompts.get("VEHICLE_ALREADY_EXISTS"))
        
        val = db.insert_item(
                sql_queries.get("insert_vehicle_by_customer_id"),
                (customer_id, vehicle_number, vehicle_type))
        return True
    
    def check_if_vehicle_exists(self, vehicle_number):
        """Check if the vehicle exists in the database
        Args:
            vehicle_number (str): The vehicle number of the vehicle to be checked
        Returns: True if the vehicle exists, False otherwise"""

        data = self.__get_vehicle_data(vehicle_number=vehicle_number)
        for vehicle in data:
            if vehicle[4] == vehicle_number:
                return True
        return False

    def __get_vehicle_data(self, vehicle_number='', customer_id='', email_address=''):
        """Fetch vehicle data from the database
        Args:
            vehicle_number (str): The vehicle number of the vehicle to be fetched
            customer_id (int): The customer id of the customer to whom the vehicle belongs
            email_address (str): The email address of the customer to whom the vehicle belongs
        Returns: The vehicle data in the form of a list of tuples"""

        try:
            vehicle_data = db.get_multiple_items(sql_queries.get("fetch_vehicle_data"),
                                                      (vehicle_number, customer_id, email_address))
            return vehicle_data
        except Exception as exc:
            raise ResourceWarning(prompts.get(
                "CANNOT_FETCH_VEHICLE_DATA")) from exc
