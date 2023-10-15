from unittest.mock import MagicMock, patch
from src.controllers.vehicle import Vehicle


import unittest


class TestVehicle(unittest.TestCase):

    def setUp(self):
        self.vehicle = Vehicle()
        self.vehicle_data = [
            (1, 1, 'LMV', 1, 'RJ20CD7259'),
        ]

    @patch('src.controllers.vehicle.db')
    def test_add_vehicle_success(self, mock_db): 
        mock_db.insert_item.return_value = True    
        self.vehicle.check_if_vehicle_exists = MagicMock(return_value = False)
        self.assertEqual(self.vehicle.add_vehicle('RJ20CD7259', 'LMV', 1), True)


    @patch('src.controllers.vehicle.db')
    def test_add_vehicle_failure(self, mock_db): 
        mock_db.insert_item.return_value = True    
        self.vehicle.check_if_vehicle_exists = MagicMock(return_value = True)
        self.assertRaises(ValueError, self.vehicle.add_vehicle, 'RJ20CD7259', 'LMV', 1)

    @patch.object(Vehicle, '_Vehicle__get_vehicle_data', new_callable=MagicMock)
    def test_check_if_vehicle_exists_success(self, mock_get_vehicle_data):

        mock_get_vehicle_data.return_value = self.vehicle_data
        self.assertEqual(self.vehicle.check_if_vehicle_exists('RJ20CD7259'), True)
        self.vehicle._Vehicle__get_vehicle_data.assert_called()

    @patch.object(Vehicle, '_Vehicle__get_vehicle_data', new_callable=MagicMock)
    def test_check_if_vehicle_exists_failure(self, mock_get_vehicle_data):

        mock_get_vehicle_data.return_value = []
        self.assertEqual(self.vehicle.check_if_vehicle_exists('RJ20CD7722'), False)
        self.vehicle._Vehicle__get_vehicle_data.assert_called()
    

    @patch('src.controllers.vehicle.db')
    def test_get_vehicle_data_success(self, mock_db):
        mock_db.get_multiple_items.return_value = self.vehicle_data
        self.assertEqual(self.vehicle._Vehicle__get_vehicle_data(vehicle_number='RJ20CD7259'), self.vehicle_data)
        self.assertEqual(self.vehicle._Vehicle__get_vehicle_data(customer_id=1), self.vehicle_data)
        self.assertEqual(self.vehicle._Vehicle__get_vehicle_data(email_address = "test@gmail.com"), self.vehicle_data)

    
    @patch('src.controllers.vehicle.db')
    def test_get_vehicle_data_failure(self, mock_db):
        mock_db.get_multiple_items.side_effect = Exception("Error")
        self.assertRaises(ResourceWarning, self.vehicle._Vehicle__get_vehicle_data, vehicle_number='RJ20CD7259')