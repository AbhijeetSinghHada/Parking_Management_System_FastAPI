import logging
import hashlib
from src.helpers.helpers import convert_user_details_to_dict
from src.models.database import db
from src.configurations.config import prompts, sql_queries
logger = logging.getLogger(__name__)


class Login:
    def __init__(self, username, password):
        self.username = username
        self.password = Login.get_hashed_password(password)
        self.user_data = None
        self.user_id = None

    def fetch_user_roles(self):
        """Fetch user roles from the database
        Returns: User roles in the form of a dictionary"""

        self.user_data = db.get_multiple_items(
            sql_queries.get("fetch_user_details"), (self.user_id,))
        self.user_data = convert_user_details_to_dict(self.user_data)
        return self.user_data

    def authenticate(self):
        """Authenticate the user
        Returns: The user id of the user if the user is authenticated"""

        data = db.get_multiple_items(
            sql_queries.get("fetch_login_details"), (self.username, self.password))
        if data:
            self.user_id = data[0][0]
            return self.user_id

        raise ValueError(prompts.get("INVALID_DETAILS"))

    @staticmethod
    def get_hashed_password(password):
        """Hash the password
        Args:
            password (str): The password to be hashed
        Returns: The hashed password"""

        password = password.encode()
        return hashlib.sha256(password).hexdigest()

