from jsonschema import ValidationError
from src.helpers import validations
from unittest.mock import patch
from unittest.mock import MagicMock
from unittest import TestCase

test_schema = {
    "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "number"},
            },
    "required": ["name", "age"],
}


class TestValidators(TestCase):

    def test_validate_vehicle_number(self):
        assert validations.validate_vehicle_number("RJ20CD7259") == True

    def test_validate_invalid_vehicle_number(self):
        with self.assertRaises(ValueError):
            assert validations.validate_vehicle_number("RJ20CD729")

    def test_validate_integer_input(self):
        assert validations.validate_integer_input(2) == True

    def test_validate_invalid_integer_input(self):
        with self.assertRaises(ValueError):
            assert validations.validate_integer_input("2a")

    def test_validate_string_input(self):
        assert validations.validate_string_input("abc") == True

    def test_validate_invalid_string_input(self):
        with self.assertRaises(ValueError):
            assert validations.validate_string_input("abc1")

    def test_validate_phone_number(self):
        assert validations.validate_phone_number(1234567890) == True

    def test_validate_invalid_phone_number(self):
        with self.assertRaises(ValueError):
            assert validations.validate_phone_number(123456789)

    def test_validate_email(self):
        assert validations.validate_email("abhi22hada@gmail.com") == True

    def test_validate_invalid_email(self):
        with self.assertRaises(ValueError):
            assert validations.validate_email("abhi22hada@gmail")

    def test_validate_request_data(self):

        request_data = {"name": "Abhi", "age": 22}  # good input
        assert validations.validate_request_data(
            request_data, test_schema) == None
        # writing string instead of integer
        request_data = {"name": "Abhi", "age": "22"}
        assert validations.validate_request_data(
            request_data, test_schema) == "'22' is not of type 'number'"

        request_data = {"name": 1234, "age": 22}  # name is not string
        assert validations.validate_request_data(
            request_data, test_schema) == "1234 is not of type 'string'"

    def test_validate_invalid_request_data(self):

        request_data = {"name": "Abhi"}  # age is mising here
        assert validations.validate_request_data(
            request_data, test_schema) == "'age' is a required property"
