import unittest
from controllers import employees
from unittest.mock import patch


class TestEmployees(unittest.TestCase):

    @patch("init_db.get_session")
    def test_read_all(self, mock_get_session):
        mock_get_session.return_value = MockEmployee()
        self.assertEqual(employees.read_all()[0], employee_data)


    @patch("init_db.get_session")
    def test_read_one(self, mock_get_session):
        existing_employee = employee_data[0]

        # Case 1: employee is found
        mock_get_session.return_value = MockEmployee(existing_employee)
        response = employees.read_one(existing_employee.get("id"))
        self.assertEqual(response[0], existing_employee)

        # Case 2: employee not found
        mock_get_session.return_value = MockEmployee()
        response = employees.read_one(existing_employee.get("id"))
        self.assertEqual(response[0], {'error': 'Employee not found for id: 1'})

    @patch("init_db.get_session")
    def test_update(self, mock_get_session):
        existing_employee_updated = employee_data[0]
        existing_employee_updated["name"] = "John"

        # Case 1: employee is found
        mock_get_session.return_value = MockEmployee(existing_employee_updated)
        response = employees.update(1, existing_employee_updated)
        self.assertEqual(response[0], existing_employee_updated)

        # Case 2: employee not found
        mock_get_session.return_value = MockEmployee()
        response = employees.update(1, existing_employee_updated)
        self.assertEqual(response[0], {'error': 'Employee not found for id: 1'})

    @patch("init_db.get_session")
    def test_delete(self, mock_get_session):
        employee_to_delete = employee_data[0]

        # Case 1: employee is found
        mock_get_session.return_value = MockEmployee(employee_to_delete)
        response = employees.delete(1)
        self.assertEqual(response[0], employee_to_delete)

        # Case 2: employee not found
        mock_get_session.return_value = MockEmployee()
        response = employees.delete(1)
        self.assertEqual(response[0], {'error': 'Employee not found for id: 1'})


class MockEmployee:
    def __init__(self, employee=None):
        self.employee = employee

    def query(self, *args, **kwargs):
        return self

    def order_by(self, *args, **kwargs):
        return self

    def filter(self, *args, **kwargs):
        return self

    def add(self, *args, **kwargs):
        return self

    def all(self, *args, **kwargs):
        return employee_data

    def commit(self, *args, **kwargs):
        return self

    def merge(self, *args, **kwargs):
        return self

    def filter_by(self, *args, **kwargs):
        return self

    def first(self, *args, **kwargs):
        return self

    def one_or_none(self, *args, **kwargs):
        return self.employee

    def delete(self, *args, **kwargs):
        return self


employee_data = [
    {
        "id": 1,
        "name": "Nabil",
        "contact_number": 123,
        "email": "mohammad@gmail.com"
    }
]
