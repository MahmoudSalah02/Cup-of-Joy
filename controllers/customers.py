"""
This is the customers module and supports all the REST actions for the
Customer table
"""

from models.models import Customer
import init_db
from models.schemas import CustomerSchema, OrderSchema


def read_all():
    """
    This function responds to a request for /api/customers
    with the complete lists of customers
    :return: array of JSON objects of all customers
    """
    session = init_db.get_session()
    # Create the list of customers from our data
    customers = session.query(Customer).order_by(Customer.name).all()

    # Serialize the data for the response
    customer_schema = CustomerSchema(many=True)
    customer_data = customer_schema.dump(customers)
    return customer_data


def create(body):
    """
    This function creates a new customer based on the customer
    data passed in
    :param body: JSON object containing new changes to customer
    :return: JSON object of the new customer
    """
    session = init_db.get_session()
    existing_customer = (
        session.query(Customer).filter(Customer.contact_number == body.get("contact_number"))
        .one_or_none()
    )

    # if customer does not exist in the database
    if existing_customer is None:

        # deserialize customer to a database object
        customer_schema = CustomerSchema()
        new_customer_deserialized = customer_schema.load(body, session=session)

        # add the customer to the database
        session.add(new_customer_deserialized)
        session.commit()

        customer_data = customer_schema.dump(new_customer_deserialized)
        return customer_data, 201

    # otherwise, person exists already
    else:
        return {"error": f"Customer {body.get('name')} exists already"}, 404


def read_one(customer_id):
    """
    This function responds to a request for /api/customers/{customer_id}
    with one matching customer from the database
    :param customer_id: id of customer to find
    :return: JSON object of the customer matching the id
    """
    session = init_db.get_session()
    existing_customer = (
        session.query(Customer).filter(Customer.id == customer_id)
        .one_or_none()
    )

    if existing_customer is not None:
        customer_schema = CustomerSchema()
        customer_data_serialized = customer_schema.dump(existing_customer)
        return customer_data_serialized

    else:
        return {"error": f"Customer not found for Id: {customer_id}"}, 404


def read_orders(customer_id):
    """
    This function returns all the order of the customer specified
    :param customer_id: id of the customer who placed orders
    :return: orders of the customer with the specified id
    """
    session = init_db.get_session()
    existing_customer = read_one(customer_id)
    customer_schema = CustomerSchema()
    existing_customer_deserialized = customer_schema.load(existing_customer, session=session)

    order_schema = OrderSchema(many=True)
    orders_data = order_schema.dump(existing_customer_deserialized.orders_placed)
    return orders_data


def update(customer_id, body):
    """
    This function updates an existing customer in the database
    :param customer_id: id of customer to update
    :param body: JSON object containing new changes to customer
    :return:
    """
    session = init_db.get_session()
    read_one(customer_id)

    # deserialize data into a database object
    customer_schema = CustomerSchema()
    existing_customer_deserialized = customer_schema.load(body, session=session)

    session.merge(existing_customer_deserialized)
    session.commit()

    body["customer_id"] = customer_id
    return body, 200


def delete(customer_id):
    """
    This function deletes an existing customer in the database
    :param customer_id: id of the customer to be deleted
    :return: JSON object containing information about the customer deleted
    """
    session = init_db.get_session()
    existing_customer = read_one(customer_id)

    # deserialize customer to a database object
    customer_schema = CustomerSchema()
    customer_schema_deserialized = customer_schema.load(existing_customer, session=session)

    # if the execution reaches this line, then existing customer is not None
    session.delete(customer_schema_deserialized)
    session.commit()
    return existing_customer
