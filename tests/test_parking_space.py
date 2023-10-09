from src.controllers.parking_space import ParkingSpace
from unittest.mock import Mock
import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class TestParkingSpace(unittest.TestCase):

    def setUp(self):
        self.db_helper = Mock()
        self.parking_space = ParkingSpace(self.db_helper)

    def test_update_parking_space(self):
        self.db_helper.update_parking_capacity.return_value = None
        self.parking_space.update_parking_capacity(20, 'LMV')
        return_val = self.db_helper.update_parking_capacity(20, 'LMV')
        self.assertEqual(return_val, None)

    def test_update_parking_charges(self):

        self.db_helper.update_charges.return_value = None
        self.parking_space.update_parking_charges(20, 'LMV')
        return_val = self.db_helper.update_charges(100, 'LMV')
        self.assertEqual(return_val, None)

    def test_get_parking_slot_attributes(self):
        self.db_helper.get_vehicle_category_data.return_value = [
            ('LMV', 20, 100), ('HMV', 10, 200), ('Two Wheeler', 30, 50)]
        return_val = self.parking_space.get_parking_category_details('LMV')
        self.assertEqual(return_val, ('LMV', 20, 100))

    def test_are_vehicles_already_parked_positive(self):
        self.db_helper.get_slots_data.return_value = [
            (11, 20, 'LMV'), (2, 10, 'HMV'), (3, 30, 'Two Wheeler')]
        return_val = self.parking_space.is_space_occupied('LMV', 10)
        self.assertEqual(return_val, True)

    def test_are_vehicles_already_parked_negative(self):
        self.db_helper.get_slots_data.return_value = [
            (11, 20, 'LMV'), (2, 10, 'HMV'), (3, 30, 'Two Wheeler')]
        return_val = self.parking_space.is_space_occupied(
            'Wheeler', 30)
        self.assertEqual(return_val, False)
