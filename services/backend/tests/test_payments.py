import unittest
from controllers import payments
from unittest.mock import patch


class TestItem(unittest.TestCase):

    @patch("init_db.get_session")
    def test_read_all(self, mock_get_session):
        mock_get_session.return_value = MockPayment()
        response = payments.read_all()
        self.assertEqual(response[0], payment_data)

    @patch('init_db.get_session')
    def test_read_one(self, mock_get_session):
        # Case 1: Payment found
        mock_get_session.return_value = MockPayment(payment_data[0])
        response = payments.read_one(payment_data[0].get("order_id"))
        self.assertEqual(response[0], payment_data[0])

        # Case 2: Payment not found
        mock_get_session.return_value = MockPayment()
        response = payments.read_one(payment_data[0].get("order_id"))
        self.assertEqual(response[0], {"error": f"Payment not found for Id: 1"})

    # TODO: payments.create() was not tested:
    # Because MockPayment returns a dictionary object instead of a DB object
    # Which does not incorporate foreign key relationships, for example
    # order.items_ordered cannot be accessed if order is a dict not a db object


class MockPayment:
    def __init__(self, payment=None):
        self.payment = payment

    def query(self, *args, **kwargs):
        return self

    def order_by(self, *args, **kwargs):
        return self

    def filter(self, *args, **kwargs):
        return self

    def add(self, *args, **kwargs):
        return self

    def all(self, *args, **kwargs):
        return payment_data

    def commit(self, *args, **kwargs):
        return self

    def one_or_none(self, *args, **kwargs):
        return self.payment


payment_data = [
    {
        "order_id": 1,
        "customer_id": 1,
        "employee_id": 1,
        "price": "$12.99"
    },
    {
        "order_id": 2,
        "customer_id": 2,
        "employee_id": 3,
        "price": "$19.99"
    },
]
