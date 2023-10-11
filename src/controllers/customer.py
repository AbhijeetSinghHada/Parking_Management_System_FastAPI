from src.helpers.helpers import get_sql_queries
from src.models.database import db
import logging
logger = logging.getLogger(__name__)
sql_queries = get_sql_queries()


class Customer:
    def __init__(self, name, email_address, phone_number, customer_id=''):
        self.customer_id = customer_id
        self.name = name
        self.email_address = email_address
        self.phone_number = phone_number

    def fetch_customer_data(self, customer_id, email_address, phone_number):
        logger.debug(
            f"fetch_customer_data called with params {customer_id},{email_address},{phone_number}")
        try:
            customer_data = db.get_multiple_items(
                sql_queries.get("fetch_customer_data"),
                (customer_id, email_address, phone_number))
            return customer_data
        except Exception as exc:
            raise ResourceWarning("Cannot Fetch Customer Data.") from exc
