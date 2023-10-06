import logging
from src.helpers import helpers
from src.helpers.helpers import return_date_time_combined, return_current_date_time
prompts = helpers.get_prompts()
logger = logging.getLogger(__name__)


class Billing:
    def __init__(self, db_helper):
        self.sql_queries = helpers.get_sql_queries()
        self.db_helper = db_helper


    @staticmethod
    def calculate_charges(charges: int, hours_parked_for):
        logger.debug("calculate_charges called with params {},{}".format(
            charges, hours_parked_for))
        if hours_parked_for > 0:
            total_charges = hours_parked_for * charges
            return total_charges
        return 1 * charges

    def generate_bill(self, bill_id):
        logger.debug("generate_bill called with params {}".format(bill_id))
        bill_data = self.db_helper.get_billing_details(bill_id)

        if not bill_data:
            logger.critical(prompts["prompts"]["BILL_ID_NOT_EXISTS"])
            raise LookupError(prompts["prompts"]["BILL_ID_NOT_EXISTS"])
        
        bill = list(bill_data[0])
        _date = bill[7]
        _time = bill[8]
        date_time = return_date_time_combined(_date, _time)
        bill[8] = date_time
        bill.pop(7)
        bill = {"customer" : {"cutomer_id": bill[1], "name": bill[2], "email_address": bill[3], "phone_number": bill[4]},
                "time_in": bill[7],
                "time_out": bill[8],
                "total_charges": bill[9]}

        return bill

    def update_bill_table(self, bill_id, charges):
        logger.debug("generate_bill called with params {}".format(bill_id))
        hours = self.db_helper.parked_time_elapsed_in_hours(bill_id)
        total_charges = self.calculate_charges(charges, hours)
        datetime_now = return_current_date_time()

        self.db_helper.update_billing_table(
            datetime_now, total_charges, bill_id)

    def insert_into_bill_table(self, vehicle_number, date, time):
        self.db_helper.insert_into_billing_table(vehicle_number, date, time)


