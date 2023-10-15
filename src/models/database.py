import logging
import mysql.connector
from src.configurations import config

logger = logging.getLogger(__name__)

class Database:
    """Database class to handle all the database operations"""

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
                logger.critical("Error: Connection not established {},"
                                " Connection Parameters : {}".format(
                    error, config.connection_parameters))
            else:
                logger.debug("Connection established")

        self.connection = Database.connection
        self.cursor = Database.cursor
        self._last = None

    def get_multiple_items(self, query, *args):
        """Fetch multiple items from the database"""

        self.cursor.execute(query, *args)
        items = self.cursor.fetchall()

        return items

    def update_item(self, query, *args):
        """Update an item in the database"""

        self.cursor.execute(query, *args)
        last = self.cursor.lastrowid
        self.connection.commit()

        return last

    def insert_item(self, query, *args):
        """Insert an item in the database"""

        self.cursor.execute(query, *args)
        last = self.cursor.lastrowid
        self.connection.commit()

        return last

    def delete_item(self, query, *args):
        """Delete an item from the database"""

        self.cursor.execute(query, *args)
        self.connection.commit()


db = Database()
