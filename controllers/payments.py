"""
This is the orders module and supports all the REST actions for the
Payments table
"""

from models.models import Payment
from init_db import session
from models.schemas import PaymentSchema


def read_all():
    """
    This function responds to a request for /api/operations
    with the complete lists of payments (or receipts)
    :return:        json string of list of payments
    """
    # Create the list of orders from our data
    payments = session.query(Payment).all()

    # Serialize the data for the response
    payment_schema = PaymentSchema(many=True)
    payments_data = payment_schema.dump(payments)
    return payments_data


def read_one(order_id):
    """
    This function responds to a request for /api/orders/{order_id}
    with one matching order from the database
    :param order_id: id of order to find
    :return: JSON object of the order matching the id
    """
    existing_payment = (
        session.query(Payment).filter(Payment.order_id == order_id)
        .one_or_none()
    )

    if existing_payment is not None:
        payment_schema = PaymentSchema()
        payment_data_serialized = payment_schema.dump(existing_payment)
        return payment_data_serialized
    else:
        return {"error": f"Payment not found for Id: {order_id}"}, 404
