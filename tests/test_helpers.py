from src.configurations import config
from src.helpers.helpers import get_sql_queries, get_prompts, convert_user_details_to_dict, return_date_and_time, return_current_date_time
from unittest.mock import mock_open, patch
from unittest import TestCase
import datetime
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


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

    def test_get_prompts(self):
        with patch('builtins.open', mock_open(read_data='{"key": "value"}')) as m:
            assert get_prompts() == {"key": "value"}     

    def test_get_sql_queries(self):
        with patch('builtins.open', mock_open(read_data='{"key": "value"}')) as m:
            assert get_sql_queries() == {"key": "value"}
