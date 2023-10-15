import unittest
from unittest.mock import patch
from src.controllers.login import Login

class TestLogin(unittest.TestCase):
    
    @patch("src.controllers.login.db")
    def test_authenticate_success(self, mock_db):
        mock_db.get_multiple_items.return_value = [(1, "test", "Test@123")]
        login = Login("test", "Test@123")
        self.assertEqual(login.authenticate(), 1)

    @patch("src.controllers.login.db")
    def test_authenticate_failure(self, mock_db):
        mock_db.get_multiple_items.return_value = []
        login = Login("test", "Test@123")
        with self.assertRaises(ValueError):
            login.authenticate()

    @patch("src.controllers.login.db")
    def test_fetch_user_roles_success(self, mock_db):
        user_data = [("test_user", 1, "test_role1"), ("test_user", 1, "test_role_2")]
        expected_response = {'name': 'test_user', 'user_id': 1, 'role': ['test_role1', 'test_role_2']}
        mock_db.get_multiple_items.return_value = user_data
        login = Login("test", "Test@123")
        login.authenticate()
        self.assertEqual(login.fetch_user_roles(), expected_response)

    def get_hashed_password(self):

        self.assertEqual(Login.get_hashed_password("Test@123"), "8776f108e247ab1e2b323042c049c266407c81fbad41bde1e8dfc1bb66fd267e")

    