from src.controllers.parking_space import ParkingSpace
from src.helpers.errors import ConflictError
from src.models.database import db
from src.configurations.config import prompts, sql_queries


class Slot(ParkingSpace):

    def assign_slot(self, slot_number, vehicle_type, vehicle_number):
        """Assign a slot to a vehicle
        Args:
            slot_number (int): The slot number to be assigned
            vehicle_type (str): The vehicle type of the vehicle to be parked
            vehicle_number (str): The vehicle number of the vehicle to be parked"""
        
        self.is_slot_type_for_vehicle_correct(vehicle_number, vehicle_type)
        self.is_vehicle_type_existing(vehicle_type)
        self.is_slot_number_existing(slot_number, vehicle_type)
        self.__is_slot_available(slot_number, vehicle_type)
        self.__is_already_parked(vehicle_number)

        db.insert_item(sql_queries.get("insert_into_slot"),
                       (slot_number, vehicle_number, vehicle_type,))
        return True

    def unassign_slot(self, vehicle_number):
        """Unassign a slot from a vehicle
        Args:
            vehicle_number (str): The vehicle number of the vehicle to be unparked"""
        
        slot_details = self.__get_slot_details_by_vehicle(vehicle_number)

        db.delete_item(
            sql_queries.get("delete_parked_slot"), (slot_details.get("slot_id"),))
        del slot_details["slot_id"]
        return slot_details

    def ban_slot(self, slot_number, slot_type):
        """Ban a slot
        Args:
            slot_number (int): The slot number to be banned
            slot_type (str): The slot type of the slot to be banned"""

        self.is_slot_number_existing(slot_number, slot_type)
        self.__is_slot_available(slot_number, slot_type)
        db.insert_item(sql_queries.get("ban_slot"),
                       (slot_number, slot_type))
        return True

    def view_ban_slots(self):
        """Returns all the banned slots for each slot type
        Returns: The banned slots in the form of a list of dictionary"""

        data = self.__get_slots_data()
        data = [{"slot_number": x[0], "vehicle_type": x[2]}
                for x in data if x[1] == -1]
        return data
        

    def unban_slot(self, slot_number, slot_type):
        """Unban a slot
        Args:
            slot_number (int): The slot number to be unbanned
            slot_type (str): The slot type of the slot to be unbanned"""
        
        db.delete_item(
            sql_queries.get("unban_slot"), (slot_number, slot_type))
        return True

    def get_all_slot_status(self, vehicle_type):
        """Get the status of all the slots for a particular slot type
        Args:
            vehicle_type (str): The slot type of the slots to be fetched
        Returns: The status of the slots in the form of a list of dictionary"""

        slot_type_capacity = self.get_parking_capacity(vehicle_type)
        slot_data = self.__get_slots_data()
        if not slot_type_capacity:
            raise ValueError(prompts.get("INVALID_SLOT_TYPE"))
        occupied_slot_numbers = [x[0]
                                 for x in slot_data if x[2] == vehicle_type and x[1]!=-1]
        ban_slot_numbers = [x[0]
                                 for x in slot_data if x[2] == vehicle_type and x[1]==-1]        
        slot_table = []

        for i in range(1, int(slot_type_capacity) + 1):
            if i in occupied_slot_numbers:
                slot_table.append({"slot_id": i, "status": "Occupied"})
                continue
            if i in ban_slot_numbers:
                slot_table.append({"slot_id": i, "status": "Banned"})
                continue
            slot_table.append({"slot_id": i, "status": "Not_Occupied"})
        return slot_table

    def __get_slots_data(self):
        """Get the slots data from the database
        Returns: The slots data in the form of a list of tuples"""

        all_slots_data = db.get_multiple_items(
            sql_queries.get("slot_data"))
        return all_slots_data

    def __is_already_parked(self, vehicle_number):
        """Check if the vehicle is already parked
        Args:
            vehicle_number (str): The vehicle number of the vehicle to be checked
        Returns: False if the vehicle is not already parked"""

        slots_data = self.__get_slots_data()
        for slot in slots_data:
            if slot[5] == vehicle_number:
                raise ConflictError(prompts.get("VEHICLE_ALREADY_PARKED"))
        return False

    def __is_slot_available(self, slot_number, slot_type):
        """Check if the slot is available
        Args:
            slot_number (int): The slot number to be checked
            slot_type (str): The slot type of the slot to be checked"""
            
        slot_data = self.__get_slots_data()
        slot_data_by_type = [x[0] for x in slot_data if x[2] == slot_type]
        if slot_number in slot_data_by_type:
            raise ConflictError(prompts.get("SLOT_OCCUPIED"))

    def __get_slot_details_by_vehicle(self, vehicle_number):
        """Get the slot details by vehicle number
        Args:
            vehicle_number (str): The vehicle number of the vehicle to be fetched
        Returns: The slot details in the form of a dictionary"""

        slot_data = self.__get_slots_data()
        for slot in slot_data:
            if slot[5] == vehicle_number:
                slot_details = {
                    "slot_number": slot[0],
                    "vehicle_number": slot[5],
                    "vehicle_type": slot[2],
                    "slot_id": slot[7],
                    "slot_charges": slot[6],
                    "bill_id": slot[4]
                }
                return slot_details
        raise ValueError(prompts.get("VEHICLE_NOT_PARKED"))

    def is_space_occupied(self, parking_category, new_capacity):
        """Check if the parking space is occupied
        Args:
            parking_category (str): The parking category to be checked
            new_capacity (int): The new capacity of the parking category
        Returns: True if the parking space is occupied"""

        slot_data = self.__get_slots_data()
        for i in slot_data:
            if i[2] == parking_category and i[0] > new_capacity:
                return True
        return False

    def is_slot_type_for_vehicle_correct(self, vehicle_number, vehicle_type):
        """Check if the slot type for the vehicle is correct
        Args:
            vehicle_number (str): The vehicle number of the vehicle to be checked
            vehicle_type (str): The vehicle type of the vehicle to be checked
        Returns: True if the slot type for the vehicle is correct"""

        vehicle_details = db.get_multiple_items(sql_queries.get("slot_type_for_vehicle"), (vehicle_number, vehicle_type,))
        if not vehicle_details:
            raise ValueError(prompts.get("INVALID_VEHICLE_NUMBER"))
        return True