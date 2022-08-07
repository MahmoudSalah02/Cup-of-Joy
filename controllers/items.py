"""
This is the items module and supports all the REST actions for the
Item table
"""

from models.models import Item
import init_db
from models.schemas import ItemSchema


def read_all():
    """
    This function responds to a request for /api/items
    with the complete lists of items
    :return:        json string of list of items
    """
    # Create the list of items from our data
    session = init_db.get_session()
    items = session.query(Item).order_by(Item.name).all()

    # Serialize the data for the response
    item_schema = ItemSchema(many=True)
    item_data = item_schema.dump(items)
    return item_data, 200


def create(body):
    """
    This function creates a new item based on the item
    data passed in
    :param body: JSON object of the item to be created
    :return: item created if request successful, error 409 otherwise
    """
    session = init_db.get_session()
    existing_item = (
        session.query(Item).filter(Item.name == body.get("name"))
        .one_or_none()
    )

    # if item does not exist in the database
    if existing_item is None:

        # deserialize item to a database object
        item_schema = ItemSchema()
        new_item_deserialized = item_schema.load(body, session=session)

        # add the item to the database
        session.add(new_item_deserialized)
        session.commit()

        item_data = item_schema.dump(new_item_deserialized)
        return item_data, 200

    # otherwise, person exists already
    else:
        return {"error": f"Item {body.get('name')} already exists"}, 404


def read_one(item_id):
    """
    This function responds to a request for /api/items/{item_id}
    with one matching item from the database
    :param item_id: id of item to find
    :return: JSON object of the item matching the id
    """
    session = init_db.get_session()
    existing_item = (
        session.query(Item).filter(Item.id == item_id)
        .one_or_none()
    )

    if existing_item is not None:
        item_schema = ItemSchema()
        item_data_serialized = item_schema.dump(existing_item)
        return item_data_serialized, 200

    else:
        return {"error": f"Item not found for id: {item_id}"}, 404


def update(item_id, body):
    """
    This function updates an existing item in the database
    :param item_id: id of item to update
    :param body: JSON object containing new changes to the specific item
    :return: JSON object containing information about the item updated
    """
    session = init_db.get_session()
    read_one_response = read_one(item_id)
    if read_one_response[1] == 404:
        return read_one_response

    # deserialize data into a database object
    item_schema = ItemSchema()
    existing_item_deserialized = item_schema.load(body, session=session)

    session.merge(existing_item_deserialized)
    session.commit()

    body["item_id"] = item_id
    return body, 200


def delete(item_id):
    """
    This function deletes an existing item in the database
    :param item_id: id of the item to be deleted
    :return: JSON object containing information about the item deleted
    """
    session = init_db.get_session()
    existing_item = read_one(item_id)
    if existing_item[1] == 404:
        return existing_item

    # deserialize item to a database object
    item_schema = ItemSchema()
    item_schema_deserialized = item_schema.load(existing_item[0], session=session)

    # if the execution reaches this line, then existing item is not None
    session.delete(item_schema_deserialized)
    session.commit()
    return existing_item[0], 200
