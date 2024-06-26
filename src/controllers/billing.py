import logging
from src.models.database import Database
from src.helpers.helpers import (return_date_time_combined,
                                 return_current_date_time,
                                 return_no_of_hours_elapsed)
from src.configurations.config import prompts
from src.configurations.config import sql_queries
logger = logging.getLogger(__name__)
db = Database()

class Billing:

    def generate_bill(self, bill_id):
        """Generate bill for the given bill id
        Args:
            bill_id (int): The bill id of the bill to be generated
        Returns: Formatted Bill with customer details, time in, time out and total charges"""

        bill_data = self.__get_billing_details(bill_id)

        if not bill_data:
            logger.critical(prompts.get("BILL_ID_NOT_EXISTS"))
            raise LookupError(prompts.get("BILL_ID_NOT_EXISTS"))

        bill = list(bill_data[0])
        _date = bill[7]
        _time = bill[8]
        date_time = return_date_time_combined(_date, _time)
        bill[8] = date_time
        bill.pop(7)
        bill = {"customer": {"cutomer_id": bill[1],
                             "name": bill[2],
                             "email_address": bill[3],
                             "phone_number": bill[4]},
                "time_in": bill[7],
                "time_out": bill[8],
                "total_charges": bill[9]}

        return bill

    def update_bill_table(self, bill_id, charges):
        """Update the bill table with the total charges and time out
        Args:
            bill_id (int): The bill id of the bill to be updated
            charges (int): The charges for the slot type"""

        hours = self.__parked_time_elapsed_in_hours(bill_id)
        total_charges = self.calculate_charges(charges, hours)
        datetime_now = return_current_date_time()
        db.update_item(sql_queries.get("update_billing_table"),
                       (datetime_now, total_charges, bill_id))

    def insert_into_bill_table(self, vehicle_number, date, time):
        """Insert into the bill table the vehicle number, 
           date and time when vehicle parked
        Args:
            vehicle_number (str): The vehicle number of the vehicle to be parked
            date (str): The date of the vehicle to be parked
            time (str): The time of the vehicle to be parked"""

        try:
            db.insert_item(sql_queries.get("insert_into_billing_table"),
                           (vehicle_number, date, time))
        except Exception as exc:
            raise ResourceWarning(prompts.get(
                "INSERT_BILLING_DATA_ERROR")) from exc

    def __get_billing_details(self, bill_id):
        """Get the billing details from the bill table"""

        try:
            data = db.get_multiple_items(
                sql_queries.get("get_billing_details"), (bill_id,))
            return data
        except Exception as exc:
            raise ResourceWarning(prompts.get(
                "GET_BILLING_DATA_ERROR")) from exc

    def __parked_time_elapsed_in_hours(self, bill_id):
        """Get the time elapsed in hours since the vehicle was parked"""

        date_time_of_bill = db.get_multiple_items(
            sql_queries.get("get_bill_date_time"), (bill_id,))
        hours = return_no_of_hours_elapsed(
            date_time_of_bill[0][0], date_time_of_bill[0][1])
        
        return hours

    @staticmethod
    def calculate_charges(charges: int, hours_parked_for):
        """Calculate the charges for the slot type"""

        if hours_parked_for > 0:
            total_charges = hours_parked_for * charges
            return total_charges
        return 1 * charges
