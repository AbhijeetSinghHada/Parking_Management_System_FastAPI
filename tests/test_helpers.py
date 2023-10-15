
from src.helpers.helpers import (convert_user_details_to_dict, 
                                return_date_and_time, 
                                return_current_date_time,
                                return_no_of_hours_elapsed,
                                formated_error)
from unittest.mock import MagicMock, patch
from unittest import TestCase
import datetime



class TestHelpers(TestCase):

    def test_convert_user_details_to_dict(self):

        assert convert_user_details_to_dict([['Kittu', 1, 'Admin']]) == {
            'name': 'Kittu', 'user_id': 1, 'role': ['Admin']}
        assert convert_user_details_to_dict([['Kittu', 1, 'Admin'], ['Kittu', 1, 'Operator']]) == {
            'name': 'Kittu', 'user_id': 1, 'role': ['Admin', 'Operator']}
        assert convert_user_details_to_dict(
            [['Kittu', 1, 'Admin'], ['Kittu', 1, 'Operator'], ['Kittu', 1, 'Operator']]) == {
            'name': 'Kittu', 'user_id': 1, 'role': ['Admin', 'Operator', 'Operator']}

    def test_return_date_and_time(self):
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M")
        assert return_date_and_time() == (datetime.date.today(), current_time)

    def test_return_current_date_time(self):
        datetime_now = datetime.datetime.now()
        assert return_current_date_time() == datetime_now.strftime("%Y-%m-%d %H:%M")

    @patch("src.helpers.helpers.return_time_difference")
    def test_return_no_of_hours_elapsed(self, mock_return_time_difference):
        mock_return_time_difference.return_value = datetime.timedelta(minutes=60)
        assert return_no_of_hours_elapsed(datetime.date(2023,9,11),
                                            datetime.time(10,15)) == 1
        mock_return_time_difference.return_value = datetime.timedelta(minutes=140)
        assert return_no_of_hours_elapsed(datetime.datetime(2023,9,11,10,15),
                                            datetime.datetime(2023,9,11,11,15)) == 2
        mock_return_time_difference.return_value = datetime.timedelta(minutes=200)
        assert return_no_of_hours_elapsed(datetime.datetime(2023,9,11,10,15),
                                            datetime.datetime(2023,9,11,12,14)) == 3

    def test_formated_error(self):
        assert formated_error(400, "Bad Request", "error") == {
            "error": {
                "code": 400,
                "message": "Bad Request"
            },
            "status": "error"
        }
        assert formated_error(500, "Internal Server Error", "error") == {
            "error": {
                "code": 500,
                "message": "Internal Server Error"
            },
            "status": "error"
        }
        assert formated_error(401, "Unauthorized", "error") == {
            "error": {
                "code": 401,
                "message": "Unauthorized"
            },
            "status": "error"
        }
        assert formated_error(403, "Forbidden", "error") == {
            "error": {
                "code": 403,
                "message": "Forbidden"
            },
            "status": "error"
        }
        assert formated_error(409, "Conflict", "error") == {
            "error": {
                "code": 409,
                "message": "Conflict"
            },
            "status": "error"
        }
        