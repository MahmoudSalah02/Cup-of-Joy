"""
This is the items module and supports all the REST actions for the
Item table
"""

from flask import abort, make_response
from models.models import Item, session
from models.schemas import ItemSchema


def read_all():
    """
    This function responds to a request for /api/items
    with the complete lists of items
    :return:        json string of list of items
    """
    # Create the list of items from our data
    items = session.query(Item).order_by(Item.name).all()

    # Serialize the data for the response
    item_schema = ItemSchema(many=True)
    item_data = item_schema.dump(items)
    return item_data


def create(body):
    """
    This function creates a new item based on the item
    data passed in
    :param body: JSON object of the item to be created
    :return: item created if request successful, error 409 otherwise
    """
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
        return item_data, 201

    # otherwise, person exists already
    else:
        abort(409, f"Item {body.get('name')} exists already")


def read_one(item_id):
    """
    This function responds to a request for /api/items/{item_id}
    with one matching item from the database
    :param item_id: id of item to find
    :return: JSON object of the item matching the id
    """
    existing_item = (
        session.query(Item).filter(Item.id == item_id)
        .one_or_none()
    )

    if existing_item is not None:
        item_schema = ItemSchema()
        item_data_serialized = item_schema.dump(existing_item)
        return item_data_serialized

    else:
        abort(404, f"Item not found for Id: {item_id}")


def update(item_id, body):
    """
    This function updates an existing item in the database
    :param item_id: id of item to update
    :param body: JSON object containing new changes to the specific item
    :return: JSON object containing information about the item updated
    """

    read_one(item_id)

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
    existing_item = read_one(item_id)

    # deserialize item to a database object
    item_schema = ItemSchema()
    item_schema_deserialized = item_schema.load(existing_item, session=session)

    # if the execution reaches this line, then existing item is not None
    session.delete(item_schema_deserialized)
    session.commit()
    return existing_item
