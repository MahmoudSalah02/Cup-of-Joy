"""
This is the orders module and supports all the REST actions for the
Order table
"""

from datetime import datetime

from flask import abort, make_response
from models.models import Order, Customer, Employee, session
from models.schemas import OrderSchema, CustomerSchema


def read_all():
    """
    This function responds to a request for /api/orders
    with the complete lists of orders
    :return:        json string of list of orders
    """
    # Create the list of orders from our data
    orders = session.query(Order).order_by(Order.order_time).all()

    # Serialize the data for the response
    order_schema = OrderSchema(many=True)
    orders_data = order_schema.dump(orders)
    return orders_data


def create(order):
    """
    This function creates a new order based on the
    passed in order data
    :param order:  order to create
    :return:       201 on success, 406 on person exists
    """

    customer_name = order.get("customer_name")
    customer_contact_number = order.get("customer_contact_number")
    employee_contact_number = order.get("employee_contact_number")

    existing_customer = (
        session.query(Customer).filter(Customer.contact_number == customer_contact_number)
        .one_or_none()
    )

    existing_employee = (
        session.query(Employee).filter(Employee.contact_number == employee_contact_number)
        .one_or_none()
    )

    # abort if employee does not exist
    if existing_employee is None:
        abort(409, f"Employee with number {employee_contact_number} does not exist")

    # customer ordered for the first time
    if existing_customer is None:
        new_customer_dic = {
            "name": customer_name,
            "contact_number": customer_contact_number
        }
        # Create a customer instance using the schema and the passed in order details
        customer_schema = CustomerSchema()
        new_customer_deserialized = customer_schema.load(new_customer_dic, session=session)

        # Add the customer to the database
        session.add(new_customer_deserialized)
        existing_customer = new_customer_deserialized

    # synchronize the in-memory state of the Session with the database
    session.flush()

    new_order_dic = {
        "customer_id": existing_customer.id,
        "employee_id": existing_employee.id,
        "order_time": str(datetime.now()),
        "status": "Preparing"
    }
    # create an order instance using the schema and the passed in order details
    order_schema = OrderSchema()
    new_order_deserialized = order_schema.load(new_order_dic, session=session)

    # Add the order to the database
    session.add(new_order_deserialized)
    session.commit()

    new_order_serialize = order_schema.dump(new_order_deserialized)
    return new_order_serialize, 201


def read_one(order_id):
    """
    This function responds to a request for /api/orders/{order_id}
    with one matching order from the database
    :param order_id: id of order to find
    :return: order matching the id
    """
    existing_order = (
        session.query(Order).filter(Order.id == order_id)
        .one_or_none()
    )

    if existing_order is not None:
        order_schema = OrderSchema()
        order_data_serialized = order_schema.dump(existing_order)
        return order_data_serialized
    else:
        abort(404, f"Order not found for Id: {order_id}")


def update(order_id, order):
    """
    This function updates an existing order in the database
    :param order_id: id of the oder to update
    :param order: new changes to the order
    :return:
    """
    existing_order = read_one(order_id)
    existing_order["status"] = order.get("status")

    # deserialize data into a database object
    order_schema = OrderSchema()
    existing_order_deserialized = order_schema.load(existing_order, session=session)

    session.merge(existing_order_deserialized)
    session.commit()

    return existing_order, 200


def update_items(order_id, order_items):
    """
    This function updates the items in an existing order in the database
    :param order_id: id of the oder to update
    :param order_items: new changes to the items in the order
    :return:
    """
    existing_order = read_one(order_id)
    existing_order["items_ordered"] = order_items

    # deserialize data into a database object
    order_schema = OrderSchema()
    existing_order_deserialized = order_schema.load(existing_order, session=session)

    session.merge(existing_order_deserialized)
    session.commit()

    return existing_order, 200


def delete(order_id):
    """
    This function deletes an existing order in the database
    :param order_id:
    :return:
    """
    existing_order = read_one(order_id)

    # deserialize order to a database object
    order_schema = OrderSchema()
    existing_order_deserialized = order_schema.load(existing_order, session=session)

    # if the execution reaches this line, then existing order is not None
    session.delete(existing_order_deserialized)
    session.commit()
    return make_response(f"Order {order_id} deleted", 200)
