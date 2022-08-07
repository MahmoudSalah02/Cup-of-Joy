import unittest
from controllers import customers
from unittest.mock import patch


class TestCustomers(unittest.TestCase):

    @patch("init_db.get_session")
    def test_read_all(self, mock_get_session):
        mock_get_session.return_value = MockCustomer()
        self.assertEqual(customers.read_all()[0], customer_data)

    @patch("init_db.get_session")
    def test_create(self, mock_get_session):
        new_customer = {
            "name": "Mohammad",
            "contact_number": 1234,
        }
        # Case 1: Customer is found
        mock_get_session.return_value = MockCustomer(customer=customer_data[0])
        response = customers.create(new_customer)
        self.assertEqual(response[0], {'error': 'Customer Mohammad exists already'})

        # Case 2: Customer not found
        mock_get_session.return_value = MockCustomer()
        response = customers.create(new_customer)
        self.assertEqual(response[0], {'id': None,
                                       'contact_number': 1234,
                                       'name': 'Mohammad'})

    @patch("init_db.get_session")
    def test_read_one(self, mock_get_session):
        existing_customer = customer_data[0]

        # Case 1: Customer is found
        mock_get_session.return_value = MockCustomer(existing_customer)
        response = customers.read_one(existing_customer.get("id"))
        self.assertEqual(response[0], existing_customer)

        # Case 2: Customer not found
        mock_get_session.return_value = MockCustomer()
        response = customers.read_one(existing_customer.get("id"))
        self.assertEqual(response[0], {'error': 'Customer not found for Id: 1'})

    @patch("init_db.get_session")
    def test_update(self, mock_get_session):
        existing_customer_updated = customer_data[0]
        existing_customer_updated["name"] = "John"

        # Case 1: customer is found
        mock_get_session.return_value = MockCustomer(existing_customer_updated)
        response = customers.update(1, existing_customer_updated)
        self.assertEqual(response[0], existing_customer_updated)

        # Case 2: customer not found
        mock_get_session.return_value = MockCustomer()
        response = customers.update(1, existing_customer_updated)
        self.assertEqual(response[0], {'error': 'Customer not found for Id: 1'})

    @patch("init_db.get_session")
    def test_delete(self, mock_get_session):
        customer_to_delete = customer_data[0]

        # Case 1: customer is found
        mock_get_session.return_value = MockCustomer(customer_to_delete)
        response = customers.delete(1)
        self.assertEqual(response[0], customer_to_delete)

        # Case 2: customer not found
        mock_get_session.return_value = MockCustomer()
        response = customers.delete(1)
        self.assertEqual(response[0], {'error': 'Customer not found for Id: 1'})

    @patch("init_db.get_session")
    def test_read_orders(self, mock_get_session):
        customer_find_orders = customer_data[0]
        customer_find_orders["orders_placed"]: []

        # Case 1: customer is found
        mock_get_session.return_value = MockCustomer(customer_find_orders)
        response = customers.read_orders(1)
        self.assertEqual(response[0], [])

        # Case 2: customer not found
        mock_get_session.return_value = MockCustomer()
        response = customers.read_orders(1)
        self.assertEqual(response[0], {'error': 'Customer not found for Id: 1'})


class MockCustomer:
    def __init__(self, customer=None):
        self.customer = customer
        self.orders_placed = []

    def query(self, *args, **kwargs):
        return self

    def order_by(self, *args, **kwargs):
        return self

    def filter(self, *args, **kwargs):
        return self

    def add(self, *args, **kwargs):
        return self

    def all(self, *args, **kwargs):
        return customer_data

    def commit(self, *args, **kwargs):
        return self

    def merge(self, *args, **kwargs):
        return self

    def filter_by(self, *args, **kwargs):
        return self

    def first(self, *args, **kwargs):
        return self

    def one_or_none(self, *args, **kwargs):
        return self.customer

    def delete(self, *args, **kwargs):
        return self


customer_data = [
    {
        "id": 1,
        "name": "Nabil",
        "contact_number": 123,
    }
]
