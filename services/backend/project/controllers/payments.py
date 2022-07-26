"""
This is the orders module and supports all the REST actions for the
Payments table
"""

from models import models, schemas
import init_db
from controllers import orders
from models.schemas import OrderSchema
from decimal import Decimal


def read_all():
    """
    This function responds to a request for /api/operations
    with the complete lists of payments (or receipts)
    :return:        json string of list of payments
    """
    session = init_db.get_session()
    # Create the list of orders from our data
    payments = session.query(models.Payment).all()

    # Serialize the data for the response
    payment_schema = schemas.PaymentSchema(many=True)
    payments_data = payment_schema.dump(payments)
    return payments_data, 200


def read_one(order_id):
    """
    This function responds to a request for /api/orders/{order_id}
    with one matching order from the database
    :param order_id: id of order to find
    :return: JSON object of the order matching the id
    """
    session = init_db.get_session()
    existing_payment = (
        session.query(models.Payment).filter(models.Payment.order_id == order_id)
        .one_or_none()
    )

    if existing_payment is not None:
        payment_schema = schemas.PaymentSchema()
        payment_data_serialized = payment_schema.dump(existing_payment)
        return payment_data_serialized, 200
    else:
        return {"error": f"Payment not found for Id: {order_id}"}, 404


def create(order_id):

    session = init_db.get_session()

    existing_payment = read_one(order_id)
    if existing_payment[1] == 200:
        return {"error": f"order {order_id} has been paid"}

    existing_order = session.query(models.Order).filter(models.Order.id == order_id).one_or_none()
    if not existing_order:
        return {"error": f"Order with id {order_id} not found"}, 404

    price = 0
    for orderItem in existing_order.items_ordered:
        item_details = orderItem.item_details
        if str(item_details.price).startswith("$") and is_float(str(item_details.price)[1:]):
            price += Decimal(item_details.price.strip('$')) * orderItem.quantity
        else:
            return {"error": "price should be in '$00.00' format"}

    new_payment = {
        "order_id": existing_order.id,
        "customer_id": existing_order.customer_id,
        "employee_id": existing_order.employee_id,
        "price": "$" + str(price)
    }

    payment_schema = schemas.PaymentSchema()
    payment_db = payment_schema.load(new_payment, session=session)
    session.add(payment_db)
    session.commit()
    return new_payment, 200


def is_float(num):
    try:
        float(num)
        return True
    except ValueError:
        return False
