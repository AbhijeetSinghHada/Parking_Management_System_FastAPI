from src.controllers.vehicle import Vehicle
from unittest.mock import Mock
import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class TestVehicle(unittest.TestCase):

    def setUp(self):
        self.db_helper = Mock()
        self.vehicle = Vehicle(self.db_helper)

    def test_check_if_vehicle_exists_positive(self):
        self.db_helper.get_vehicle_data.return_value = [
            (1, 'Kittu', 'kittu@gmail.com', '1234567890', 'RJ20CD7259', 'LMV')]

        data = self.vehicle.check_if_vehicle_exists('RJ20CD7259')
        self.assertEqual(data, [
            (1, 'Kittu', 'kittu@gmail.com', '1234567890', 'RJ20CD7259', 'LMV')])

    def test_check_if_vehicle_exists_negative(self):
        self.db_helper.get_vehicle_data.return_value = []

        data = self.vehicle.check_if_vehicle_exists('RJ20CD7259')
        self.assertEqual(data, None)

    def test_add_vehicle(self):
        self.db_helper.insert_vehicle.return_value = None
        self.vehicle.add_vehicle('RJ20CD7259', 'LMV')
        return_val = self.db_helper.insert_vehicle('RJ20CD7259', 'LMV')
        self.assertEqual(return_val, None)

    def test_add_vehicle_category(self):
        self.db_helper.add_vehicle_category.return_value = None
        self.vehicle.add_vehicle_category('LMV', 20, 100)
        return_val = self.db_helper.add_vehicle_category('LMV', 20, 100)
        self.assertEqual(return_val, None)



if __name__ == '__main__':
    unittest.main()
