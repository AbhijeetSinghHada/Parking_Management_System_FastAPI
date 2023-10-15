import logging
from src.models.database import db
from src.configurations.config import prompts, sql_queries

logger = logging.getLogger(__name__)


class ParkingSpace:

    def add_parking_category(self, slot_type, total_capacity, parking_charge):
        """Add a new parking category
        Args:
            slot_type (str): The slot type of the parking category to be added
            total_capacity (int): The total capacity of the parking category to be added
            parking_charge (int): The parking charge of the parking category to be added"""

        db.update_item(
            sql_queries.get("add_vehicle_type"),
            (slot_type, total_capacity, parking_charge))
        return True

    def update_parking_capacity(self, new_capacity, parking_category):
        """Update the parking capacity of a parking category
        Args:
            new_capacity (int): The new capacity of the parking category
            parking_category (str): The parking category to be updated"""

        db.update_item(
            sql_queries.get("update_vehicle_capacity"),
            (new_capacity, parking_category))
        return True

    def update_parking_charges(self, new_charges, parking_category):
        """Update the parking charges of a parking category
        Args:
            new_charges (int): The new charges of the parking category
            parking_category (str): The parking category to be updated"""

        db.update_item(
            sql_queries.get("update_vehicle_charges"),
            (new_charges, parking_category))
        return True

    def parking_space_details(self):
        """Fetch the parking space details
        Returns: The parking space details in the form of a list of dictionary"""

        data = self.__get_parking_space_details()
        vehicle_data = [
            {"slot_type": i[0],
             "total_capacity": i[1],
             "charge": i[2]} for i in data]
        return vehicle_data

    def get_parking_category_details(self, parking_category):
        """Fetch the parking category details
        Args:
            parking_category (str): The parking category to be fetched
        Returns: The parking category details in the form of a list"""

        vehicle_category_data = self.__get_parking_space_details()
        parking_category_data = None
        for i in vehicle_category_data:
            if parking_category == i[0]:
                parking_category_data = i
        return parking_category_data

    def is_slot_number_existing(self, slot_number, parking_category):
        """Check if the slot number is existing for the parking category
        Args:
            slot_number (int): The slot number to be checked
            parking_category (str): The parking category to be checked"""

        parking_category_data = self.get_parking_category_details(parking_category)
        if slot_number > parking_category_data[1]:
            raise ValueError(prompts.get("SLOT_NUMBER_EXCEEDS_CAPACITY"))

    def is_vehicle_type_existing(self, vehicle_type):
        """Check if the vehicle type exists in the parking space
        Args:
            vehicle_type (str): The vehicle type to be checked"""

        vehicle_category_data = self.__get_parking_space_details()
        for i in vehicle_category_data:
            if vehicle_type == i[0]:
                return True
        raise ValueError(prompts.get("VEHICLE_TYPE_NOT_FOUND"))

    def get_parking_capacity(self, vehicle_type):
        """Get the parking capacity of the vehicle type
        Args:
            vehicle_type (str): The vehicle type to be checked
        Returns: The parking capacity of the vehicle type if the vehicle type exists"""
        try:
            vehicle_category_data = self.__get_parking_space_details()
            for category in vehicle_category_data:
                if category[0] == vehicle_type:
                    return category[1]
            return False
        except Exception as exc:
            raise ResourceWarning(prompts.get("FETCH_PARKING_CAPACITY_ERROR")) from exc

    def __get_parking_space_details(self):
        """Get the parking space details for each parking category from the database
        Returns: The parking space details in the form of a list of tuples"""        
        try:
            vehicle_category_data = db.get_multiple_items(sql_queries.get("vehicle_category_data"))
            return vehicle_category_data
        except Exception as exc:
            raise ResourceWarning(prompts.get("FETCH_PARKING_SPACE_ERROR")) from exc
