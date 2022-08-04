import unittest
from controllers import items
from unittest.mock import patch


class TestItem(unittest.TestCase):

    @patch("init_db.get_session")
    def test_read_all(self, mock_get_session):
        mock_get_session.return_value = MockItem()
        self.assertEqual(items.read_all()[0], item_data)

    @patch("init_db.get_session")
    def test_create(self, mock_get_session):
        new_item = {
            "ingredients": "chicken, onions, rice",
            "name": "Curry Chicken",
            "price": "$16.99"
        }
        # Case 1: Item is found
        mock_get_session.return_value = MockItem(item=item_data[0])
        response = items.create(new_item)
        self.assertEqual(response[0], {'error': 'Item Curry Chicken already exists'})

        # Case 2: Item not found
        mock_get_session.return_value = MockItem()
        response = items.create(new_item)
        self.assertEqual(response[0], {"id": None,
                                       "ingredients": "chicken, onions, rice",
                                       "name": "Curry Chicken",
                                       "price": "$16.99"})

    @patch("init_db.get_session")
    def test_read_one(self, mock_get_session):
        existing_item = item_data[0]

        # Case 1: item is found
        mock_get_session.return_value = MockItem(existing_item)
        response = items.read_one(existing_item.get("id"))
        self.assertEqual(response[0], existing_item)

        # Case 2: item not found
        mock_get_session.return_value = MockItem()
        response = items.read_one(existing_item.get("id"))
        self.assertEqual(response[0], {'error': 'Item not found for id: 1'})

    @patch("init_db.get_session")
    def test_update(self, mock_get_session):
        existing_item_updated = item_data[0]
        existing_item_updated["name"] = "John"

        # Case 1: Item is found
        mock_get_session.return_value = MockItem(existing_item_updated)
        response = items.update(1, existing_item_updated)
        self.assertEqual(response[0], existing_item_updated)

        # Case 2: Item not found
        mock_get_session.return_value = MockItem()
        response = items.update(1, existing_item_updated)
        self.assertEqual(response[0], {'error': 'Item not found for id: 1'})

    @patch("init_db.get_session")
    def test_delete(self, mock_get_session):
        item_to_delete = item_data[0]

        # Case 1: Item is found
        mock_get_session.return_value = MockItem(item_to_delete)
        response = items.delete(1)
        self.assertEqual(response[0], item_to_delete)

        # Case 2: Item not found
        mock_get_session.return_value = MockItem()
        response = items.delete(1)
        self.assertEqual(response[0], {'error': 'Item not found for id: 1'})


class MockItem:
    def __init__(self, item=None):
        self.item = item

    def query(self, *args, **kwargs):
        return self

    def order_by(self, *args, **kwargs):
        return self

    def filter(self, *args, **kwargs):
        return self

    def add(self, *args, **kwargs):
        return self

    def all(self, *args, **kwargs):
        return item_data

    def commit(self, *args, **kwargs):
        return self

    def merge(self, *args, **kwargs):
        return self

    def filter_by(self, *args, **kwargs):
        return self

    def first(self, *args, **kwargs):
        return self

    def one_or_none(self, *args, **kwargs):
        return self.item

    def delete(self, *args, **kwargs):
        return self


item_data = [
    {
        "id": 1,
        "ingredients": "chicken, onions, rice",
        "name": "Curry Chicken with Onion",
        "price": "$7.00"
    }
]
