import logging
import traceback
from src.helpers.helpers import get_sql_queries, return_no_of_hours_elapsed

logger = logging.getLogger(__name__)


class DatabaseHelper:
    def __init__(self, db):
        self.db = db
        self.sql_queries = get_sql_queries()
        self.slots_data = None
        self.vehicle_category_data = None

    def get_slots_data(self):
        logger.debug("get_slots_data called")
        try:
            self.slots_data = self.db.get_multiple_items(
                self.sql_queries.get("slot_data"))
            return self.slots_data
        except Exception as exc:
            raise ResourceWarning("Cannot Fetch Slot Data.") from exc

    def get_parking_capacity(self, vehicle_type):
        logger.debug(f"get_parking_capacity called with params {vehicle_type}")
        try:
            self.vehicle_category_data = self.db.get_multiple_items(
                self.sql_queries.get("vehicle_category_data"))
            for i in self.vehicle_category_data:
                if i[0] == vehicle_type:
                    return i[1]
        except Exception as exc:
            raise ResourceWarning("Cannot Fetch Parking Capacity.") from exc

    def get_vehicle_category_data(self):
        logger.debug("get_vehicle_category_data called")

        try:
            self.vehicle_category_data = self.db.get_multiple_items(
                self.sql_queries.get("vehicle_category_data"))
            return self.vehicle_category_data
        except Exception as exc:
            raise ResourceWarning(
                "Cannot Fetch Vehicle Category Data.") from exc

    def update_charges(self, charges, vehicle_type):
        logger.debug(
            f"update_charges called with params {charges},{vehicle_type}")

        try:
            self.db.update_item(
                self.sql_queries.get("update_vehicle_charges"), (charges, vehicle_type))

        except Exception as exc:
            raise ResourceWarning("Cannot Update Charges.") from exc

    def update_parking_capacity(self, total_capacity, parking_category):
        logger.debug(
            f"update_parking_capacity called with params {total_capacity},{parking_category}")
        try:
            self.db.update_item(
                self.sql_queries.get("update_vehicle_capacity"), (total_capacity, parking_category))
        except Exception as exc:
            raise ResourceWarning("Cannot Update Parking Capacity.") from exc

    def add_vehicle_category(self, slot_type, total_capacity, parking_charge):
        try:
            self.db.update_item(
                self.sql_queries.get("add_vehicle_type"),
                (slot_type, total_capacity, parking_charge))
        except Exception as exc:
            raise ResourceWarning(
                "Cannot Add Vehicle to the Database.") from exc

    def parked_time_elapsed_in_hours(self, bill_id):
        logger.debug(
            f"parked_time_elapsed_in_hours called with params {bill_id}")
        date_time_of_bill = self.db.get_multiple_items(
            self.sql_queries.get("get_bill_date_time"), (bill_id,))
        hours = return_no_of_hours_elapsed(
            date_time_of_bill[0][0], date_time_of_bill[0][1])
        return hours

    def get_billing_details(self, bill_id):
        logger.debug(f"get_billing_details called with params {bill_id}")

        try:
            data = self.db.get_multiple_items(
                self.sql_queries.get("get_billing_details"), (bill_id,))
            return data
        except Exception as exc:
            raise ResourceWarning("Cannot Fetch Billing Details.") from exc

    def update_billing_table(self, datetime_now, total_charges, bill_id):
        logger.debug(
            f"update_billing_table called with params {datetime_now},{total_charges},{bill_id}")

        try:
            self.db.update_item(
                self.sql_queries.get("update_billing_table"),
                (datetime_now, total_charges, bill_id))
        except Exception as exc:
            raise ResourceWarning("Cannot Update Billing Details.") from exc

    def insert_into_billing_table(self, vehicle_number, date, time):
        logger.debug(
            f"insert_into_billing_table called with params {vehicle_number},{date},{time}")
        try:
            self.db.update_item(self.sql_queries.get("insert_into_billing_table"),
                                (vehicle_number, date, time))
        except Exception as exc:
            raise ResourceWarning("Cannot Add Billing Details.") from exc

    def insert_into_slot_table(self, slot_number, vehicle_number, vehicle_type):
        logger.debug(
            f"insert_into_slot_table called with params {slot_number},{vehicle_number},{vehicle_type}")
        try:
            self.db.update_item(self.sql_queries.get("insert_into_slot"),
                                (slot_number, vehicle_number, vehicle_type,))
        except Exception as exc:
            raise ResourceWarning("Cannot Add Slot.") from exc

    def remove_parked_slot(self, slot_id):
        logger.debug(f"remove_parked_slot called with params {slot_id}")
        try:
            self.db.update_item(
                self.sql_queries.get("delete_parked_slot"), (slot_id,))
        except Exception as exc:
            raise ResourceWarning("Cannot Remove Parked Slot.") from exc

    def ban_slot_by_slot_number(self, slot_number, vehicle_type):
        logger.debug(
            f"ban_slot_by_slot_number called with params {slot_number},{vehicle_type}")
        try:
            self.db.update_item(self.sql_queries.get("ban_slot"),
                                (slot_number, vehicle_type))
        except Exception as exc:
            raise ResourceWarning("Cannot Ban Slot.") from exc

    def unban_slot(self, slot_number, slot_type):
        logger.debug(
            f"unban_slot called with params {slot_number},{slot_type}")
        try:
            self.db.update_item(
                self.sql_queries.get("unban_slot"), (slot_number, slot_type))
        except Exception as exc:
            raise ResourceWarning("Cannot Unban Slot.") from exc

    def get_vehicle_data(self, vehicle_number='', customer_id='', email_address=''):
        logger.debug(
            f"get_vehicle_data called with params {vehicle_number},{customer_id},{email_address}")
        try:
            vehicles = self.db.get_multiple_items(self.sql_queries.get("fetch_vehicle_data"),
                                                  (vehicle_number, customer_id, email_address))
            return vehicles
        except Exception as exc:
            raise ResourceWarning("Cannot Fetch Vehicle Data.") from exc

    def fetch_customer_data(self, customer_id, email_address, phone_number):
        logger.debug(
            f"fetch_customer_data called with params {customer_id},{email_address},{phone_number}")
        try:
            customer_data = self.db.get_multiple_items(
                self.sql_queries.get("fetch_customer_data"),
                (customer_id, email_address, phone_number))
            return customer_data
        except Exception as exc:
            raise ResourceWarning("Cannot Fetch Customer Data.") from exc

    def insert_vehicle_by_customer_id(self, customer_id, vehicle_number, selected_vehicle_type):
        logger.debug(
            f"insert_vehicle_by_customer_id called with params {customer_id},{vehicle_number},{selected_vehicle_type}")
        try:
            self.db.update_item(
                self.sql_queries.get("insert_vehicle_by_customer_id"),
                (customer_id, vehicle_number, selected_vehicle_type))
        except Exception as exc:
            raise ResourceWarning("Cannot Add Vehicle.") from exc

    def insert_customer_details(self, name, email_address, phone_number):
        logger.debug(
            f"insert_customer_details called with params {name},{email_address},{phone_number}")
        try:
            return self.db.update_item(
                self.sql_queries.get("insert_customer"), (name, email_address, phone_number))
        except Exception as exc:
            logger.debug(traceback.format_exc())
            raise ResourceWarning("Cannot Add Customer.") from exc

    def insert_vehicle(self, vehicle_number, vehicle_type):
        logger.debug(
            f"insert_vehicle called with params {vehicle_number},{vehicle_type}")
        try:
            self.db.update_item(
                self.sql_queries.get("insert_vehicle"), (vehicle_number, vehicle_type))
        except Exception as exc:
            raise ResourceWarning("Cannot Add Vehicle.") from exc
