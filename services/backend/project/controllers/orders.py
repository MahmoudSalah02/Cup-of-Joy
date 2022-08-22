"""
This is the orders module and supports all the REST actions for the
Order table
"""

from sqlalchemy.exc import IntegrityError
import init_db
from controllers import customers, employees
from models import models, schemas


def read_all():
    """
    This function responds to a request for /api/orders
    with the complete lists of orders
    :return:        json string of list of orders
    """
    session = init_db.get_session()
    # Create the list of orders from our data
    orders = session.query(models.Order).order_by(models.Order.order_time).all()

    # Serialize the data for the response
    order_schema = schemas.OrderSchema(many=True)
    orders_data = order_schema.dump(orders)
    return orders_data, 200


def create(body):
    """
    This function creates a new order based on the
    passed in order data
    :param body:  order to create
    :return:       201 on success, 406 on person exists
    """
    session = init_db.get_session()
    if customers.read_one(body.get("customer_id"))[1] == 404:
        return {"error": f"Customer with Id {body.get('customer_id')} not found"}, 404

    if employees.read_one(body.get("employee_id"))[1] == 404:
        return {"error": f"Employee with Id {body.get('employee_id')} not found"}, 404

    order_schema = schemas.OrderSchema()
    new_order_deserialized = order_schema.load(body, session=session)

    try:
        session.add(new_order_deserialized)
        session.commit()
        session.flush()
    except IntegrityError:
        return {"error": "order item not found for one or more inserted items"}

    new_order_serialize = order_schema.dump(new_order_deserialized)
    return new_order_serialize, 200


def read_one(order_id):
    """
    This function responds to a request for /api/orders/{order_id}
    with one matching order from the database
    :param order_id: id of order to find
    :return: JSON object of the order matching the id
    """
    session = init_db.get_session()
    existing_order = (
        session.query(models.Order).filter(models.Order.id == order_id)
        .one_or_none()
    )

    if existing_order is not None:
        order_schema = schemas.OrderSchema()
        order_data_serialized = order_schema.dump(existing_order)
        return order_data_serialized, 200
    else:
        return {"error": f"Order not found for Id: {order_id}"}, 404


def update(order_id, body):
    """
    This function updates an existing order in the database
    :param order_id: id of the oder to update
    :param body: JSON object containing new changes to the order
    :return: JSON object of the updated order
    """
    session = init_db.get_session()

    existing_order = read_one(order_id)

    if existing_order[1] == 404:
        return {"error": f"Order not found for Id: {order_id}"}, 404

    if customers.read_one(body.get("customer_id"))[1] == 404:
        return {"error": f"Order not found for Id: {body.get('customer_id')}"}, 404

    if employees.read_one(body.get("employee_id"))[1] == 404:
        return {"error": f"Employee not found for Id: {body.get('employee_id')}"}, 404

    body["id"] = order_id
    order_schema = schemas.OrderSchema()
    existing_order_deserialized = order_schema.load(body, session=session)
    session.merge(existing_order_deserialized)

    new_order_serialize = order_schema.dump(existing_order_deserialized)

    session.commit()
    return new_order_serialize, 200


def delete(order_id):
    """
    This function deletes an existing order in the database
    :param order_id: ID of the order to delete
    :return: JSON object of the deleted order
    """
    session = init_db.get_session()

    existing_order = read_one(order_id)
    if existing_order[1] == 404:
        return existing_order

    # deserialize order to a database object
    order_schema = schemas.OrderSchema()
    existing_order_deserialized = order_schema.load(existing_order[0], session=session)

    # if the execution reaches this line, then existing order is not None
    session.delete(existing_order_deserialized)
    session.commit()
    return existing_order[0], 200
