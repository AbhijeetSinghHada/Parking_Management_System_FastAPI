from src.helpers.logger import log
import mysql.connector
from src.configurations import config
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

    @log(logger=logger)
    def get_multiple_items(self, query, *args):
        self.cursor.execute(query, *args)
        items = self.cursor.fetchall()

        return items

    @log(logger=logger)
    def update_item(self, query, *args):
        self.cursor.execute(query, *args)
        last = self.cursor.lastrowid
        self.connection.commit()

        return last


db = Database()
