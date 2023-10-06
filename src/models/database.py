import mysql.connector
from src.configurations import config
from src.controllers.slot import Slot
import logging
logger = logging.getLogger(__name__)


class Database:
    connection = None
    cursor = None

    def __init__(self):
        self.last = None
        if Database.connection is None:
            try:
                Database.connection = mysql.connector.connect(
                    **config.connection_parameters)
                Database.cursor = Database.connection.cursor()
            except Exception as error:
                logger.critical("Error: Connection not established {}, Connection Parameters : {}".format(
                    error, config.connection_parameters))
            else:
                logger.debug("Connection established")

        self.connection = Database.connection
        self.cursor = Database.cursor
        self._last = None

    def get_multiple_items(self, query, *args):
        self.cursor.execute(query, *args)
        items = self.cursor.fetchall()
        logger.debug("get_multiple_item called with params {} returned item : {} ".format(args,items))

        return items

    def update_item(self, query, *args):
        self.cursor.execute(query, *args)
        last = self.cursor.lastrowid
        self.connection.commit()
        logger.debug("update_item called with params {} returned item : {}, ".format(args, last))

        return last


if __name__ == "__main__":
    he = Database()
    slot = Slot(he)
    slot.generate_bill('11')
