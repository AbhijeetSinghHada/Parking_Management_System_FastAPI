import unittest
from unittest.mock import MagicMock, patch
from src.controllers.slot import Slot
from src.helpers.errors import ConflictError



class TestSlot(unittest.TestCase):


    def setUp(self):
        self.slot = Slot()

        self.slot_data= [
        (1, -1, 'LMV', 1, -1, '0', 100, 49),
        (5, -1, 'LMV', 1, -1, '0', 100, 50),
        (2, -1, 'HMV', 1, -1, '0', 50,  51),
        (7, 1, 'LMV',  2, 79, 'RJ20CD7259', 100, 47),
        (4, 13, 'LMV', 2, 81, 'RJ91BW7711', 100, 48),
        ]

    @patch.object(Slot, '_Slot__is_already_parked', new_callable=MagicMock)
    @patch.object(Slot, '_Slot__is_slot_available', new_callable=MagicMock)
    @patch('src.controllers.slot.db', new_callable=MagicMock)
    def test_assign_slot(self, mock_db, mock_is_slot_available, mock_is_already_parked):
        self.slot.is_vehicle_type_existing = MagicMock(return_value=True)
        self.slot.is_slot_number_existing = MagicMock(return_value=True)
        mock_is_slot_available.return_value = True
        mock_is_already_parked.return_value = True

        mock_db.insert_item.return_value = True
        self.assertEqual(self.slot.assign_slot(1, 'LMV', 'RJ20CD7259'), True)
        self.slot.is_vehicle_type_existing.assert_called_once_with('LMV')
        self.slot.is_slot_number_existing.assert_called_once_with(1, 'LMV')
        mock_is_slot_available.assert_called_once_with(1, 'LMV')
        mock_is_already_parked.assert_called_once_with('RJ20CD7259')

    

    @patch('src.controllers.slot.db', new_callable=MagicMock)
    @patch.object(Slot, '_Slot__get_slot_details_by_vehicle', new_callable=MagicMock)
    def test_unassign_slot(self, mock_get_slot_details_by_vehicle, mock_db):
        return_data = {"slot_number": 1, 
                       "vehicle_number": "RJ20CD7259", 
                       "vehicle_type": "LMV", 
                       "slot_id": 1, 
                       "slot_charges": 100, 
                       "bill_id": 1}
        mock_get_slot_details_by_vehicle.return_value = return_data
        mock_db.delete_item.return_value = True
        self.assertEqual(self.slot.unassign_slot('RJ20CD7259'), return_data)
        mock_get_slot_details_by_vehicle.assert_called_once_with('RJ20CD7259')
        mock_db.delete_item.assert_called_once()


    @patch('src.controllers.slot.db', new_callable=MagicMock)
    @patch.object(Slot, '_Slot__is_slot_available', new_callable=MagicMock)
    def test_ban_slot(self, mock_is_slot_available, mock_db):
        self.slot.is_slot_number_existing = MagicMock(return_value=True)
        mock_is_slot_available.return_value = True
        mock_db.insert_item.return_value = True

        self.assertEqual(self.slot.ban_slot(1, 'TEST'), True)
        self.slot.is_slot_number_existing.assert_called_once_with(1, 'TEST')
        mock_is_slot_available.assert_called_once_with(1, 'TEST')

    @patch.object(Slot, '_Slot__get_slots_data', new_callable=MagicMock)
    def test_view_ban_slots(self, mock_get_slots_data):
        mock_get_slots_data.return_value = self.slot_data
        self.assertEqual(self.slot.view_ban_slots(), [{'slot_number': 1, 'vehicle_type': 'LMV'},
                                                      {'slot_number': 5, 'vehicle_type': 'LMV'},
                                                      {'slot_number': 2, 'vehicle_type': 'HMV'}])
        mock_get_slots_data.assert_called_once()
    

    @patch('src.controllers.slot.db', new_callable=MagicMock)
    def test_unban_slot(self, mock_db):
        mock_db.delete_item.return_value = True
        self.assertEqual(self.slot.unban_slot(1, 'LMV'), True)
        mock_db.delete_item.assert_called_once()
        

    @patch.object(Slot, '_Slot__get_slots_data', new_callable=MagicMock)
    def test_get_all_slot_status(self, mock_get_slots_data):
        mock_get_slots_data.return_value = self.slot_data
        self.slot.get_parking_capacity = MagicMock(return_value=8)
        self.assertEqual(self.slot.get_all_slot_status('LMV'), [{'slot_id': 1, 'status': 'Occupied'},
                                                                {'slot_id': 2, 'status': 'Not Occupied'},
                                                                {'slot_id': 3, 'status': 'Not Occupied'},
                                                                {'slot_id': 4, 'status': 'Occupied'},
                                                                {'slot_id': 5, 'status': 'Occupied'},
                                                                {'slot_id': 6, 'status': 'Not Occupied'},
                                                                {'slot_id': 7, 'status': 'Occupied'},
                                                                {'slot_id': 8, 'status': 'Not Occupied'}])
        mock_get_slots_data.assert_called_once()
    
    @patch.object(Slot, '_Slot__get_slots_data', new_callable=MagicMock)
    def test_get_all_slot_status_invalid(self, mock_get_slots_data):
        mock_get_slots_data.return_value = self.slot_data
        self.slot.get_parking_capacity = MagicMock(return_value=False)
        
        with self.assertRaises(ValueError):
            self.slot.get_all_slot_status('LMV')
        mock_get_slots_data.assert_called_once()

    @patch('src.controllers.slot.db', new_callable=MagicMock)
    def test_get_slots_data(self, mock_db):
        mock_db.get_multiple_items.return_value = 1
        self.assertEqual(self.slot._Slot__get_slots_data(), 1)
        mock_db.get_multiple_items.assert_called_once()
    
    
    @patch.object(Slot, '_Slot__get_slots_data', new_callable=MagicMock)
    def test_is_already_parked_success(self, mock_get_slots_data):
        mock_get_slots_data.return_value = self.slot_data
        with self.assertRaises(ConflictError):
            self.slot._Slot__is_already_parked('RJ20CD7259')
        mock_get_slots_data.assert_called_once()

        
    @patch.object(Slot, '_Slot__get_slots_data', new_callable=MagicMock)
    def test_is_already_parked_failed(self, mock_get_slots_data):
        mock_get_slots_data.return_value = self.slot_data

        self.assertEqual(self.slot._Slot__is_already_parked('IN20VV_1234'), False)
        mock_get_slots_data.assert_called_once()

    @patch.object(Slot, '_Slot__get_slots_data', new_callable=MagicMock)
    def test_is_slot_available_success(self, mock_get_slots_data):
        mock_get_slots_data.return_value = self.slot_data
        
        with self.assertRaises(LookupError):
            self.slot._Slot__is_slot_available(1, 'LMV')
        
        mock_get_slots_data.assert_called_once()
    
    @patch.object(Slot, '_Slot__get_slots_data', new_callable=MagicMock)
    def test_is_slot_available_failed(self, mock_get_slots_data):
        mock_get_slots_data.return_value = self.slot_data
        
        self.assertEqual(self.slot._Slot__is_slot_available(3, 'LMV'), None)
        mock_get_slots_data.assert_called_once()

    @patch.object(Slot, '_Slot__get_slots_data', new_callable=MagicMock)
    def test_get_slot_details_by_vehicle_success(self, mock_get_slots_data):
        mock_get_slots_data.return_value = self.slot_data
        self.assertEqual(self.slot._Slot__get_slot_details_by_vehicle('RJ20CD7259'), 
                         {'slot_number': 7, 'vehicle_number': 'RJ20CD7259', 'vehicle_type': 'LMV', 'slot_id': 47, 'slot_charges': 100, 'bill_id': 79})
        mock_get_slots_data.assert_called_once()
    
    @patch.object(Slot, '_Slot__get_slots_data', new_callable=MagicMock)
    def test_get_slot_details_by_vehicle_failure(self, mock_get_slots_data):
        mock_get_slots_data.return_value = self.slot_data
        with self.assertRaises(ValueError):
            self.slot._Slot__get_slot_details_by_vehicle('RJ20CD7250')
        mock_get_slots_data.assert_called_once()

    @patch.object(Slot, '_Slot__get_slots_data', new_callable=MagicMock)
    def test_is_space_occupied_success(self, mock_get_slots_data):
        mock_get_slots_data.return_value = self.slot_data
        self.assertEqual(self.slot.is_space_occupied('LMV', 6), True)
        mock_get_slots_data.assert_called_once()
    
    @patch.object(Slot, '_Slot__get_slots_data', new_callable=MagicMock)
    def test_is_space_occupied_failure(self, mock_get_slots_data):
        mock_get_slots_data.return_value = self.slot_data
        self.assertEqual(self.slot.is_space_occupied('LMV', 10), False)
        mock_get_slots_data.assert_called_once()
if __name__ == '__main__':
    unittest.main()
