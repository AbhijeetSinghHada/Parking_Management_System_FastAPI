import unittest
from unittest.mock import patch
from unittest.mock import MagicMock
from src.helpers.driver_program import ProgramDriver


class TestDriverProgram(unittest.TestCase):
    def setUp(self):
        self.db_helper = MagicMock()
        self.program_driver = ProgramDriver(self.db_helper)

    @patch('src.controllers.parking_space.ParkingSpace.check_if_vehicle_type_exists')
    @patch('src.controllers.parking_space.ParkingSpace.check_if_slot_in_range')
    @patch('src.controllers.parking_space.ParkingSpace.check_if_slot_already_occupied')
    @patch('src.controllers.slot.Slot.check_if_vehicle_exists')
    @patch('src.controllers.slot.Slot.assign_slot')
    @patch('src.controllers.billing.Billing.insert_into_bill_table')
    def test_assign_slot(self, mock_check_if_vehicle_type_exists,
                         mock_check_if_slot_in_range,
                         mock_check_if_vehicle_exists,
                         mock_check_if_slot_already_occupied,
                         mock_assign_slot,
                         mock_insert_into_bill_table):

        mock_check_if_vehicle_type_exists.return_value = True
        mock_check_if_slot_in_range.return_value = True
        mock_check_if_slot_already_occupied.return_value = True
        mock_check_if_vehicle_exists.return_value = [
            (1, 'Ram', 'ram@gmail.com', '1234567899', 'RJ20CD7259', 'LMV')]
        mock_assign_slot.return_value = None
        mock_insert_into_bill_table.return_value = None
        self.assertTrue(self.program_driver.assign_slot(
            8, 'LMV', 'RJ20CD7259'))

        mock_check_if_vehicle_exists.return_value = None
        with self.assertRaises(ValueError):
            self.program_driver.assign_slot(8, 'LMV', 'RJ20CD7259')

        with self.assertRaises(ValueError):
            self.program_driver.assign_slot(8, 'HMV', 'RJ20CD7259')

    @patch('src.controllers.slot.Slot.get_slot_data_by_slot_type')
    def test_get_slot_table_by_category(self, mock_get_slot_data_by_slot_type):

        mock_get_slot_data_by_slot_type.return_value = [{'slot_id': 1, 'status': 'Occupied'}, {'slot_id': 2, 'status': 'Not Occupied'}, {
            'slot_id': 3, 'status': 'Occupied'}, {'slot_id': 4, 'status': 'Not Occupied'}, {'slot_id': 5, 'status': 'Occupied'}]
        self.assertEqual(self.program_driver.get_slot_table_by_category('LMV'),  [{'slot_id': 1, 'status': 'Occupied'}, {'slot_id': 2, 'status': 'Not Occupied'}, {
                         'slot_id': 3, 'status': 'Occupied'}, {'slot_id': 4, 'status': 'Not Occupied'}, {'slot_id': 5, 'status': 'Occupied'}])

    @patch('src.models.database_helpers.DatabaseHelper.insert_customer_details')
    @patch('src.models.database_helpers.DatabaseHelper.fetch_customer_data')
    @patch('src.controllers.parking_space.ParkingSpace.check_if_vehicle_type_exists')
    @patch('src.controllers.vehicle.Vehicle.check_if_vehicle_exists')
    def test_add_vehicle(self, mock_check_if_vehicle_exists,
                         mock_check_if_vehicle_type_exists,
                         mock_fetch_customer_data,
                         mock_insert_customer_details):
        return_data = {'customer': {'customer_id': 1, 'name': 'Ram', 'email_address': 'ram@gmail.com',
                                    'phone_number': '1234567899'}, 'vehicle_number': 'RJ20CD7259', 'vehicle_type': 'LMV'}
        return_msg = "Vehicle Added Successfully. Customer Details Existed."
        mock_check_if_vehicle_exists.return_value = False
        mock_check_if_vehicle_type_exists.return_value = True
        mock_insert_customer_details.return_value = 1
        mock_fetch_customer_data.return_value = [
            (1, 'Ram', 'ram@gmail.com', '1234567899')]
        self.assertEqual(self.program_driver.add_vehicle(
            'RJ20CD7259', 'LMV', 1, 'Ram', 'ram@gmail.com', '1234567899'), (return_data, return_msg))

        mock_fetch_customer_data.return_value = []
        return_msg = "Vehicle Added Successfully. Customer Details Added."
        self.assertEqual(self.program_driver.add_vehicle(
            'RJ20CD7259', 'LMV', 1, 'Ram', 'ram@gmail.com', '1234567899'), (return_data, return_msg))

    @patch('src.models.database_helpers.DatabaseHelper.get_slots_data')
    @patch('src.controllers.billing.Billing.update_bill_table')
    @patch('src.controllers.slot.Slot.unassign_slot')
    @patch('src.controllers.billing.Billing.generate_bill')
    @patch('src.controllers.billing.Billing.insert_into_bill_table')
    @patch('src.controllers.slot.Slot.check_if_vehicle_exists')
    def test_unassign_slot(self, mock_check_if_vehicle_exists,
                           mock_insert_into_bill_table,
                           mock_generate_bill,
                           mock_unassign_slot,
                           mock_update_bill_table,
                           mock_get_slots_data):

        mock_check_if_vehicle_exists.return_value = [
            (1, 'Ram', 'ram@gmail.com', '1234567899', 'RJ20CD7259', 'LMV')]
        mock_insert_into_bill_table.return_value = None
        mock_generate_bill.return_value = {
            "customer": {
                "cutomer_id": 1,
                "name": "Ram",
                "email_address": "ram@gmail.com",
                "phone_number": "1234567899"
            },
            "time_in": "2023-10-08T13:22:00",
            "time_out": "2023-10-08T15:53:00",
            "total_charges": 20
        }
        mock_update_bill_table.return_value = True
        mock_unassign_slot.return_value = None
        mock_get_slots_data.return_value = [(7, -1, 'LMV', 1, -1, '0', 10, 17), (2, -1, 'LMV', 1, -1, '0', 10, 18),
                                            (4, -1, 'LMV', 1, -1, '0', 10, 19), (6, 1, 'LMV', 2, 10, 'RJ20CD7259', 10, 20)]
        self.assertEqual(self.program_driver.unassign_slot('RJ20CD7259'), (
            {'slot_number': 6, 'vehicle_number': 'RJ20CD7259', 'vehicle_type': 'LMV'}, {
                "customer": {
                    "cutomer_id": 1,
                    "name": "Ram",
                    "email_address": "ram@gmail.com",
                    "phone_number": "1234567899"
                },
                "time_in": "2023-10-08T13:22:00",
                "time_out": "2023-10-08T15:53:00",
                "total_charges": 20
            }))

        mock_get_slots_data.return_value = [(7, -1, 'LMV', 1, -1, '0', 10, 17), (2, -1, 'LMV', 1, -1, '0', 10, 18),
                                            (4, -1, 'LMV', 1, -1, '0', 10, 19), (6, 1, 'LMV', 2, 10, 'RJ20CD7259', 10, 20)]
        with self.assertRaises(ValueError):
            self.program_driver.unassign_slot(
                'RJ20CD7590')  # Wrong Vehicle Number

    @patch('src.models.database_helpers.DatabaseHelper.get_vehicle_category_data')
    def test_check_parking_capacity(self, mock_get_vehicle_category_data):
        mock_get_vehicle_category_data.return_value = [
            ('LMV', 20, 100), ('HMV', 10, 200)]
        self.assertEqual(
            self.program_driver.check_parking_capacity(), [
                {
                    "slot_type": "LMV",
                    "total_capacity": 20,
                    "charge": 100
                },
                {
                    "slot_type": "HMV",
                    "total_capacity": 10,
                    "charge": 200
                }])

    @patch('src.models.database_helpers.DatabaseHelper.get_vehicle_category_data')
    @patch('src.controllers.vehicle.Vehicle.add_vehicle_category')
    def test_add_vehicle_category(self, mock_add_vehicle_category,
                                  mock_get_vehicle_category_data):
        mock_add_vehicle_category.return_value = None
        mock_get_vehicle_category_data.return_value = [
            ('LMV', 20, 100), ('HMV', 10, 200), ('Bike', 15, 10)]

        with self.assertRaises(LookupError):
            self.program_driver.add_vehicle_category('LMV', 15, 99)

        with self.assertRaises(ValueError):
            self.program_driver.add_vehicle_category('Cycle', -1, 99)

        with self.assertRaises(ValueError):
            self.program_driver.add_vehicle_category('Cycle', 15, -1)

        self.assertTrue(
            self.program_driver.add_vehicle_category('Cycle', 15, 100))

    @patch("src.controllers.parking_space.ParkingSpace.get_parking_slot_attributes")
    def test_update_parking_space(self, mock_get_parking_slot_attributes):
        mock_get_parking_slot_attributes.return_value = [
            'LMV', 20, 100]
        self.assertTrue(self.program_driver.update_parking_space(15, 'LMV'))

        mock_get_parking_slot_attributes.return_value = []
        with self.assertRaises(ValueError):
            self.program_driver.update_parking_space(15, 'HMV')

        mock_get_parking_slot_attributes.return_value = [
            'LMV', 20, 100]
        with self.assertRaises(ValueError):
            self.program_driver.update_parking_space(-1, 'LMV')

    @patch('src.controllers.parking_space.ParkingSpace.check_if_slot_in_range')
    @patch('src.controllers.parking_space.ParkingSpace.check_if_slot_already_occupied')
    def test_ban_slot(self, mock_check_if_slot_in_range, mock_check_if_slot_already_occupied):
        mock_check_if_slot_in_range.return_value = True
        mock_check_if_slot_already_occupied.return_value = True
        self.assertTrue(self.program_driver.ban_slot(1, 'LMV'))

    @patch('src.controllers.slot.Slot.view_ban_slots')
    def test_view_ban_slots(self, mock_view_ban_slots):
        mock_view_ban_slots.return_value = [
            {
                "slot_number": 7,
                "vehicle_type": "LMV"
            },
            {
                "slot_number": 2,
                "vehicle_type": "LMV"
            },
            {
                "slot_number": 4,
                "vehicle_type": "LMV"
            }
        ]
        self.assertEqual(self.program_driver.view_ban_slots(), [
            {
                "slot_number": 7,
                "vehicle_type": "LMV"
            },
            {
                "slot_number": 2,
                "vehicle_type": "LMV"
            },
            {
                "slot_number": 4,
                "vehicle_type": "LMV"
            }
        ])

    @patch('src.controllers.slot.Slot.unban_slot')
    def test_unban_slot(self, mock_unban_slot):
        mock_unban_slot.return_value = True
        self.assertTrue(self.program_driver.unban_slot(1, 'LMV'))

    @patch('src.controllers.parking_space.ParkingSpace.update_parking_charges')
    def test_update_parking_charges(self, mock_update_parking_charges):
        mock_update_parking_charges.return_value = True
        self.assertTrue(self.program_driver.update_parking_charges(100, 'LMV'))
