import unittest
from controllers import login
from unittest.mock import patch


class TestLogin(unittest.TestCase):

    @patch("init_db.get_session")
    def test_process_registration(self, mock_get_session):

        # Case 1: Username already exists
        mock_get_session.return_value = MockLogin(login_info[0])
        response = login.process_registration_request(login_info[0])
        self.assertEqual(response[0], {'error': 'admin already exists'})

        # Case 2: Registration successful
        mock_get_session.return_value = MockLogin()
        response = login.process_registration_request(login_info[0])
        employee_without_credentials = {
            'id': None,
            'name': 'Mahmoud',
            'contact_number': 123,
            'email': 'Mahhmoud@gmail.com',
            'role': 'manager'
        }
        self.assertEqual(response[0], employee_without_credentials)


class MockLogin:
    def __init__(self, employee=None):
        self.employee = employee

    def query(self, *args, **kwargs):
        return self

    def filter(self, *args, **kwargs):
        return self

    def add(self, *args, **kwargs):
        return self

    def all(self, *args, **kwargs):
        return login_info

    def commit(self, *args, **kwargs):
        return self

    def one_or_none(self, *args, **kwargs):
        return self.employee


login_info = [
    {
        "name": "Mahmoud",
        "contact_number": 123,
        "email": "Mahhmoud@gmail.com",
        "role": "manager",
        "username": "admin",
        "password": "123"
    }
]
