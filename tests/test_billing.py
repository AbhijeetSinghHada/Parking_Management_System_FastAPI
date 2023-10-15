import datetime
import unittest
from unittest.mock import MagicMock, patch
from src.controllers.billing import Billing

class TestBilling(unittest.TestCase):

    def setUp(self):
        self.billing = Billing()
        self.sql_queries = {
            "test_queries" : "test"
        }
        

    def test_calculate_charges_hours_more_than_zero(self):
        return_value = self.billing.calculate_charges(20, 12)
        self.assertEqual(return_value, 240)
        return_value = self.billing.calculate_charges(0, 12)
        self.assertEqual(return_value, 0)

    def test_calculate_charges_hours_zero(self):
        return_value = self.billing.calculate_charges(20, 0)
        self.assertEqual(return_value, 20)

    def test_calculate_charges_hours_less_than_zero(self):
        return_value = self.billing.calculate_charges(40, -2)
        self.assertEqual(return_value, 40)

    @patch('src.helpers.helpers.return_date_time_combined', new_callable=MagicMock)
    @patch.object(Billing, '_Billing__get_billing_details', new_callable=MagicMock)
    def test_generate_bill_with_existing_id(self, mock_get_billing_details, mock_return_date_time_combined):
        mock_data = [(12, 1, 'Ram', 'ram@gmail.com', '1234567899', 'RJ20CD7259',
                      'LMV', datetime.date(2023, 9, 11), datetime.timedelta(minutes=615), datetime.datetime(2023, 9, 11, 10, 15), 25)]
        mock_return_date_time_combined.return_value = datetime.datetime(2023, 9, 11, 10, 15)
        mock_get_billing_details.return_value=mock_data

        bill_id = 1
        bill = self.billing.generate_bill(bill_id)
        expected_bill = {'customer': {'cutomer_id': 1,
                                      'name': 'Ram',
                                      'email_address': 'ram@gmail.com',
                                      'phone_number': '1234567899'},
                         'time_in': datetime.datetime(2023, 9, 11, 10, 15),
                         'time_out': datetime.datetime(2023,9, 11, 10, 15),
                         'total_charges': 25
                         }
        self.assertEqual(bill, expected_bill)

    @patch.object(Billing, '_Billing__get_billing_details', new_callable=MagicMock)
    def test_generate_bill_with_non_existing_id(self, mock_get_billing_details):
        mock_get_billing_details.return_value= []
        bill_id = 999  
        with self.assertRaises(LookupError):
            self.billing.generate_bill(bill_id)

    @patch.object(Billing,'_Billing__parked_time_elapsed_in_hours', new_callable=MagicMock)
    @patch('src.controllers.billing.db', new_callable=MagicMock)
    def test_update_bill_table(self, mock_db,  mock_parked_time_elapsed_in_hours):
        
        mock_db.update_item.return_value = 1
        mock_parked_time_elapsed_in_hours.return_value = 2
        response = self.billing.update_bill_table(1, 20)
        self.assertEqual(response, None)

    @patch('src.controllers.billing.db', new_callable=MagicMock)
    def test_insert_into_bill_table_success(self, mock_db):
        mock_db.insert_item.return_value = 1
        response = self.billing.insert_into_bill_table("RJ20CD7259", "2023-09-11", "10:15")
        self.assertEqual(response, None)

    @patch('src.controllers.billing.db', new_callable=MagicMock)
    def test_insert_into_bill_table_failure(self, mock_db):
        mock_db.insert_item.side_effect = Exception("Error")
        with self.assertRaises(Exception):
            self.billing.insert_into_bill_table("RJ20CD7259", "2023-09-11", "10:15")

    @patch('src.controllers.billing.db', new_callable=MagicMock)
    def test_get_billing_details_success(self, mock_db):
        mock_db.get_multiple_items.return_value = [(12, 1, 'Ram', 'ram@gmail.com', '1234567899', 'RJ20CD7259',
                      'LMV', datetime.date(2023, 9, 11), datetime.timedelta(minutes=615), datetime.datetime(2023, 9, 11, 10, 15), 25)]
        response = self.billing._Billing__get_billing_details(1)
        self.assertEqual(response, [(12, 1, 'Ram', 'ram@gmail.com', '1234567899', 'RJ20CD7259',
                      'LMV', datetime.date(2023, 9, 11), datetime.timedelta(minutes=615), datetime.datetime(2023, 9, 11, 10, 15), 25)])
        
    @patch('src.controllers.billing.db', new_callable=MagicMock)
    def test_get_billing_details_failure(self, mock_db):
        mock_db.get_multiple_items.side_effect = Exception("Error")
        
        with self.assertRaises(ResourceWarning):
            self.billing._Billing__get_billing_details(1)

    @patch('src.controllers.billing.return_no_of_hours_elapsed', new_callable=MagicMock)
    @patch('src.controllers.billing.db', new_callable=MagicMock)
    def test_parked_time_elapsed_in_hours(self, mock_db, mock_return_no_of_hours_elapsed):
        mock_db.get_multiple_items.return_value = [(datetime.datetime(2023, 9, 11), datetime.timedelta(minutes=130))]
        mock_return_no_of_hours_elapsed.return_value = 2
        response = self.billing._Billing__parked_time_elapsed_in_hours(1)
        self.assertEqual(response, 2)

if __name__ == '__main__':

    unittest.main()

