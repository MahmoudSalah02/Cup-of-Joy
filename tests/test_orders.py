import unittest
from controllers import orders
from unittest.mock import patch


class TestOrder(unittest.TestCase):

    @patch("init_db.get_session")
    def test_read_all(self, mock_get_session):
        mock_get_session.return_value = MockOrder()
        self.assertEqual(orders.read_all()[0], order_data)

    @patch("init_db.get_session")
    def test_create(self, mock_get_session):
        new_order = {
            "id": 2,
            "customer_id": 2,
            "employee_id": 2,
            "items_ordered": [
                {
                    "customer_notes": "extra salt",
                    "item_id": 2,
                    "quantity": 2
                }
            ],
            "status": "preparing"
        }

        # Case 1: Order is found
        mock_get_session.return_value = MockOrder(new_order)
        response = orders.create(new_order)
        self.assertEqual(response[0], new_order)

        # Case 2: Customer not found, order should not be created
        mock_get_session.return_value = MockOrder()
        response = orders.create(new_order)
        self.assertEqual(response[0], {"error": "Customer with Id 2 not found"})

    @patch("init_db.get_session")
    def test_read_one(self, mock_get_session):
        existing_order = order_data[0]

        # Case 1: Order is found
        mock_get_session.return_value = MockOrder(existing_order)
        response = orders.read_one(existing_order.get("id"))
        self.assertEqual(response[0], existing_order)

        # Case 2: Order not found
        mock_get_session.return_value = MockOrder()
        response = orders.read_one(existing_order.get("id"))
        self.assertEqual(response[0], {'error': 'Order not found for Id: 1'})

    @patch("init_db.get_session")
    def test_update(self, mock_get_session):
        existing_order_updated = order_data[0]
        existing_order_updated["status"] = "done"

        # Case 1: Order is found
        mock_get_session.return_value = MockOrder(existing_order_updated)
        response = orders.update(1, existing_order_updated)
        self.assertEqual(response[0], existing_order_updated)

        # Case 2: Order not found
        mock_get_session.return_value = MockOrder()
        response = orders.update(1, existing_order_updated)
        self.assertEqual(response[0], {'error': 'Order not found for Id: 1'})

    @patch("init_db.get_session")
    def test_delete(self, mock_get_session):
        order_to_delete = order_data[0]

        # Case 1: Order is found
        mock_get_session.return_value = MockOrder(order_to_delete)
        response = orders.delete(1)
        self.assertEqual(response[0], order_to_delete)

        # Case 2: Order not found
        mock_get_session.return_value = MockOrder()
        response = orders.delete(1)
        self.assertEqual(response[0], {'error': 'Order not found for Id: 1'})


class MockOrder:
    def __init__(self, order=None):
        self.order = order

    def query(self, *args, **kwargs):
        return self

    def order_by(self, *args, **kwargs):
        return self

    def filter(self, *args, **kwargs):
        return self

    def add(self, *args, **kwargs):
        return self

    def all(self, *args, **kwargs):
        return order_data

    def commit(self, *args, **kwargs):
        return self

    def merge(self, *args, **kwargs):
        return self

    def filter_by(self, *args, **kwargs):
        return self

    def first(self, *args, **kwargs):
        return self

    def one_or_none(self, *args, **kwargs):
        return self.order

    def delete(self, *args, **kwargs):
        return self

    def flush(self, *args, **kwargs):
        return self


order_data = [
    {
        "id": 1,
        "customer_id": 1,
        "employee_id": 1,
        "items_ordered": [
            {
                "customer_notes": "extra salt",
                "item_id": 1,
                "quantity": 1
            }
        ],
        "status": "preparing"
    }
]
