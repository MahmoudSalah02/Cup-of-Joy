"""
This is the orders module and supports all the REST actions for the
Order table
"""

from decimal import Decimal
from controllers import customers, employees
from models.models import Order
import init_db
from models.schemas import OrderSchema, PaymentSchema


def read_all():
    """
    This function responds to a request for /api/orders
    with the complete lists of orders
    :return:        json string of list of orders
    """
    session = init_db.get_session()
    # Create the list of orders from our data
    orders = session.query(Order).order_by(Order.order_time).all()

    # Serialize the data for the response
    order_schema = OrderSchema(many=True)
    orders_data = order_schema.dump(orders)
    return orders_data


def create(body):
    """
    This function creates a new order based on the
    passed in order data
    :param body:  order to create
    :return:       201 on success, 406 on person exists
    """
    session = init_db.get_session()
    if customers.read_one(body.get("customer_id")) is None:
        return {"error": f"Order not found for Id: {body.get('customer_id')}"}, 404

    if employees.read_one(body.get("employee_id")) is None:
        return {"error": f"Order not found for Id: {body.get('employee_id')}"}, 404

    order_schema = OrderSchema()
    new_order_deserialized = order_schema.load(body, session=session)

    session.add(new_order_deserialized)
    session.flush()

    price = 0
    for orderItem in new_order_deserialized.items_ordered:
        item_details = orderItem.item_details
        price += Decimal(item_details.price.strip('$')) * orderItem.quantity

    new_payment = {
        "order_id": new_order_deserialized.id,
        "customer_id": body.get("customer_id"),
        "employee_id": body.get("employee_id"),
        "price": price
    }

    payment_schema = PaymentSchema()
    payment_schema.load(new_payment, session=session)
    session.commit()

    new_order_serialize = order_schema.dump(new_order_deserialized)
    return new_order_serialize, 201


def read_one(order_id):
    """
    This function responds to a request for /api/orders/{order_id}
    with one matching order from the database
    :param order_id: id of order to find
    :return: JSON object of the order matching the id
    """
    session = init_db.get_session()
    existing_order = (
        session.query(Order).filter(Order.id == order_id)
        .one_or_none()
    )

    if existing_order is not None:
        order_schema = OrderSchema()
        order_data_serialized = order_schema.dump(existing_order)
        return order_data_serialized
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
    if read_one(order_id) is None:
        return {"error": f"Order not found for Id: {order_id}"}, 404

    if customers.read_one(body.get("customer_id")) is None:
        return {"error": f"Order not found for Id: {body.get('customer_id')}"}, 404

    if employees.read_one(body.get("employee_id")) is None:
        return {"error": f"Employee not found for Id: {body.get('employee_id')}"}, 404

    body["id"] = order_id
    order_schema = OrderSchema()
    existing_order_deserialized = order_schema.load(body, session=session)

    session.merge(existing_order_deserialized)
    session.commit()

    new_order_serialize = order_schema.dump(existing_order_deserialized)
    return new_order_serialize, 201


def delete(order_id):
    """
    This function deletes an existing order in the database
    :param order_id: ID of the order to delete
    :return: JSON object of the deleted order
    """
    session = init_db.get_session()
    existing_order = read_one(order_id)

    # deserialize order to a database object
    order_schema = OrderSchema()
    existing_order_deserialized = order_schema.load(existing_order, session=session)

    # if the execution reaches this line, then existing order is not None
    session.delete(existing_order_deserialized)
    session.commit()
    return existing_order
