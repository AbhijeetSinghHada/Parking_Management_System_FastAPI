import unittest
from unittest.mock import MagicMock, patch
from src.controllers.parking_space import ParkingSpace


class TestParkingSpace(unittest.TestCase):

    def setUp(self):
        self.parking_space = ParkingSpace()

    @patch('src.controllers.parking_space.db', new_callable=MagicMock)
    def test_add_parking_category(self, mock_db):
        mock_db.update_item.return_value = True
        self.assertEqual(self.parking_space.add_parking_category('LMV', 20, 100), True)

    @patch('src.controllers.parking_space.db', new_callable=MagicMock)
    def test_update_parking_capacity(self, mock_db):
        mock_db.update_item.return_value = True
        self.assertEqual(self.parking_space.update_parking_capacity(20, 'LMV'), True)


    @patch('src.controllers.parking_space.db', new_callable=MagicMock)
    def test_update_parking_charges(self, mock_db):
        mock_db.update_item.return_value = True
        self.assertEqual(self.parking_space.update_parking_charges(100, 'LMV'), True)


    @patch.object(ParkingSpace, '_ParkingSpace__get_parking_space_details', new_callable=MagicMock)
    def test_parking_space_details(self, mock_get_parking_space_details):
        mock_get_parking_space_details.return_value = [('LMV', 20, 100)]
        self.assertEqual(self.parking_space.parking_space_details(), [{'slot_type': 'LMV', 'total_capacity': 20, 'charge': 100}])

        mock_get_parking_space_details.return_value = [('LMV', 20, 100), ('HMV', 20, 200)]
        self.assertEqual(self.parking_space.parking_space_details(), 
                         [{'slot_type': 'LMV', 'total_capacity': 20, 'charge': 100}, 
                          {'slot_type': 'HMV', 'total_capacity': 20, 'charge': 200}])
        
    @patch.object(ParkingSpace, '_ParkingSpace__get_parking_space_details', new_callable=MagicMock)
    def test_get_parking_category_details(self, mock_get_parking_space_details):
        mock_get_parking_space_details.return_value = [('LMV', 20, 100)]
        self.assertEqual(self.parking_space.get_parking_category_details('LMV'), ('LMV', 20, 100))

        mock_get_parking_space_details.return_value = [('LMV', 20, 100), ('HMV', 20, 200)]
        self.assertEqual(self.parking_space.get_parking_category_details('HMV'), ('HMV', 20, 200))
        
    @patch.object(ParkingSpace, '_ParkingSpace__get_parking_space_details', new_callable=MagicMock)
    def test_get_parking_category_details_with_invalid_category(self, mock_get_parking_space_details):

        mock_get_parking_space_details.return_value = [('LMV', 20, 100), ('HMV', 20, 200)]
        self.assertEqual(self.parking_space.get_parking_category_details('SMV'), None)


    def test_is_slot_number_existing(self):
        self.parking_space.get_parking_category_details = MagicMock()

        self.parking_space.get_parking_category_details.return_value = ('LMV', 20, 100)
        self.assertEqual(self.parking_space.is_slot_number_existing(20, 'LMV'), None)

        self.parking_space.get_parking_category_details.return_value = ('HMV', 8, 50)
        self.assertEqual(self.parking_space.is_slot_number_existing(4, 'HMV'), None)

    def test_is_slot_number_existing_with_invalid_slot_number(self):
        self.parking_space.get_parking_category_details = MagicMock()
        self.parking_space.get_parking_category_details.return_value = ('Bike', 4, 20)
        with self.assertRaises(ValueError):
            self.parking_space.is_slot_number_existing(5, 'Bike')

    @patch.object(ParkingSpace, '_ParkingSpace__get_parking_space_details', new_callable=MagicMock) 
    def test_is_slot_type_existing(self, mock_get_parking_space_details):
        mock_get_parking_space_details.return_value = [('LMV', 20, 100), ('HMV', 20, 200)]

        self.assertEqual(self.parking_space.is_vehicle_type_existing('LMV'), True)

        self.assertEqual(self.parking_space.is_vehicle_type_existing('HMV'), True)

    @patch.object(ParkingSpace, '_ParkingSpace__get_parking_space_details', new_callable=MagicMock)
    def test_is_slot_type_existing_with_invalid_slot_type(self, mock_get_parking_space_details):
        mock_get_parking_space_details.return_value = [('LMV', 20, 100), ('HMV', 20, 200)]
        with self.assertRaises(ValueError):
            self.parking_space.is_vehicle_type_existing('Bike')


    @patch.object(ParkingSpace, '_ParkingSpace__get_parking_space_details', new_callable=MagicMock) 
    def test_get_parking_capacity(self, mock_get_parking_space_details):
        mock_get_parking_space_details.return_value = [('LMV', 20, 100), 
                                                       ('HMV', 8, 200), 
                                                       ('Bike', 4, 20)]
        
        self.assertEqual(self.parking_space.get_parking_capacity('LMV'), 20)
        self.assertEqual(self.parking_space.get_parking_capacity('HMV'), 8)
        self.assertEqual(self.parking_space.get_parking_capacity('Car'), False)

    
    @patch.object(ParkingSpace, '_ParkingSpace__get_parking_space_details', new_callable=MagicMock) 
    def test_get_parking_capacity_invalid(self, mock_get_parking_space_details):
        mock_get_parking_space_details.return_value = [('LMV', 20, 100), 
                                                       ('HMV', 8, 200), 
                                                       ('Bike', 4, 20)]
        
        mock_get_parking_space_details.side_effect = ValueError('Error')
        with self.assertRaises(ResourceWarning):
            self.parking_space.get_parking_capacity('Car')

    @patch('src.controllers.parking_space.db', new_callable=MagicMock)
    def test_get_parking_space_details(self, mock_db):
        mock_db.get_multiple_items.return_value = [('LMV', 20, 100), 
                                                   ('HMV', 8, 200), 
                                                   ('Bike', 4, 20)]
        self.assertEqual(self.parking_space._ParkingSpace__get_parking_space_details(), 
                         [('LMV', 20, 100), 
                          ('HMV', 8, 200), 
                          ('Bike', 4, 20)])

    @patch('src.controllers.parking_space.db', new_callable=MagicMock)
    def test_get_parking_space_details_invalid(self, mock_db):
        mock_db.get_multiple_items.side_effect = ValueError('Error')
        with self.assertRaises(ResourceWarning):
            self.parking_space._ParkingSpace__get_parking_space_details()