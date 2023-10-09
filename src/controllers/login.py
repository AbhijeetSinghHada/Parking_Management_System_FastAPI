import logging
import hashlib
from src.helpers import helpers

prompts = helpers.get_prompts()
logger = logging.getLogger(__name__)


class Login:
    def __init__(self, db, username, password):
        self.username = username
        self.password = Login.get_hashed_password(password)
        self.user_id = None
        self.user_data = None
        self.db = db
        self.sql_queries = helpers.get_sql_queries()

    def fetch_user_roles(self):
        self.user_data = self.db.get_multiple_items(
            self.sql_queries.get("fetch_user_details"), (self.user_id,))
        self.user_data = helpers.convert_user_details_to_dict(self.user_data)
        return self.user_data

    def authenticate(self):
        data = self.db.get_multiple_items(
            self.sql_queries.get("fetch_login_details"), (self.username, self.password))
        if data:
            self.user_id = data[0][0]
            return self.user_id

        raise ValueError(prompts.get(
            "prompts").get("INVALID_DETAILS"))

    @staticmethod
    def get_hashed_password(password):
        password = password.encode()
        return hashlib.sha256(password).hexdigest()


if __name__ == '__main__':
    Login.get_hashed_password("Abhi2233")
