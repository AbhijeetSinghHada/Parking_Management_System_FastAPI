import traceback
from src.models.database import db
import logging
from src.configurations.config import sql_queries, prompts
from src.helpers.logger import log
logger = logging.getLogger(__name__)


class Customer:

    @log(logger=logger)
    def fetch_customer_data(self, customer_id, email_address, phone_number):
        try:
            customer_data = db.get_multiple_items(
                sql_queries.get("fetch_customer_data"),
                (customer_id, email_address, phone_number))
            return customer_data
        except Exception as exc:
            raise ResourceWarning(prompts.get(
                "FETCH_CUSTOMER_DATA_ERROR"))

    @log(logger=logger)
    def insert_customer_details(self, name, email_address, phone_number):
        try:
            return db.update_item(
                sql_queries.get("insert_customer"), (name, email_address, phone_number))
        except Exception as exc:
            logger.debug(traceback.format_exc())
            raise ResourceWarning(prompts.get(
                "INSERT_CUSTOMER_ERROR"))
