import logging
import mysql.connector
from src.configurations import config

logger = logging.getLogger(__name__)

class Database:
    """Database class to handle all the database operations"""

    connection = None
    cursor = None

    def __init__(self):
        if Database.connection is None:
            Database.establish_connection()

        self.connection = Database.connection
        self.cursor = Database.cursor
        self.last = None


    def get_multiple_items(self, query, *args):
        """Fetch multiple items from the database"""
        try:
            self.cursor.execute(query, *args)
            items = self.cursor.fetchall()
            return items
        except Exception as error:
            Database.reset()
            raise error

    def update_item(self, query, *args):
        """Update an item in the database"""
        try:
            self.cursor.execute(query, *args)
            last = self.cursor.lastrowid
            self.connection.commit()

            return last
        except Exception as error:
            Database.reset()
            raise error

    def insert_item(self, query, *args):
        """Insert an item in the database"""
        try:
            self.cursor.execute(query, *args)
            last = self.cursor.lastrowid
            self.connection.commit()

            return last
        except Exception as error:
            Database.reset()
            raise error

    def delete_item(self, query, *args):
        """Delete an item from the database"""
        try:
            self.cursor.execute(query, *args)
            self.connection.commit()
        except Exception as error:
            Database.reset()
            raise error


    @classmethod
    def reset(cls):
        """Reset the database connection"""

        cls.connection = None
        cls.cursor = None
        cls.establish_connection()

    @classmethod
    def establish_connection(cls):
        """Establish a connection with the database"""

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
        


db = Database()
