import logging
from src.models.database import db
from src.configurations.config import sql_queries, prompts
logger = logging.getLogger(__name__)


class Customer:

    def fetch_customer_data(self, customer_id, email_address, phone_number):
        """Fetch customer data from the database
        Args:
            customer_id (int): The customer id of the customer to be fetched
            email_address (str): The email address of the customer to be fetched
            phone_number (str): The phone number of the customer to be fetched
        Returns: Customer data in the form of a list if any of the 
                 args match to customer in the database"""

        try:
            customer_data = db.get_multiple_items(
                sql_queries.get("fetch_customer_data"),
                (customer_id, email_address, phone_number))
            return customer_data
        except Exception as exc:
            raise ResourceWarning(prompts.get(
                "FETCH_CUSTOMER_DATA_ERROR")) from exc

    def insert_customer_details(self, name, email_address, phone_number):
        """Insert customer details into the database
        Args:
            name (str): The name of the customer to be inserted
            email_address (str): The email address of the customer to be inserted
            phone_number (str): The phone number of the customer to be inserted
        Returns: The customer id of the customer inserted"""

        try:
            customer_id =  db.update_item(
                sql_queries.get("insert_customer"), (name, email_address, phone_number))
            return customer_id
        
        except Exception as exc:
            raise ResourceWarning(prompts.get(
                "INSERT_CUSTOMER_ERROR")) from exc
