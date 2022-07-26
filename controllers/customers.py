"""
This is the customers module and supports all the REST actions for the
Customer table
"""

from flask import abort
from models.models import Customer, session
from models.schemas import CustomerSchema


def read_all():
    """
    This function responds to a request for /api/customers
    with the complete lists of customers
    :return:        json string of list of customers
    """
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
    :param body:
    :return:
    """
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
        abort(409, f"Customer {body.get('name')} exists already")


def read_one(customer_id):
    """
    This function responds to a request for /api/customers/{customer_id}
    with one matching customer from the database
    :param customer_id: id of customer to find
    :return: customer matching the id
    """
    existing_customer = (
        session.query(Customer).filter(Customer.id == customer_id)
        .one_or_none()
    )

    if existing_customer is not None:
        customer_schema = CustomerSchema()
        customer_data_serialized = customer_schema.dump(existing_customer)
        return customer_data_serialized

    else:
        abort(404, f"Customer not found for Id: {customer_id}")


def update(customer_id, body):
    """
    This function updates an existing customer in the database
    :param customer_id: id of customer to update
    :param body: new changes to the customer
    :return:
    """

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
    :return:
    """
    existing_customer = read_one(customer_id)

    # deserialize customer to a database object
    customer_schema = CustomerSchema()
    customer_schema_deserialized = customer_schema.load(existing_customer, session=session)

    # if the execution reaches this line, then existing customer is not None
    session.delete(customer_schema_deserialized)
    session.commit()
    return existing_customer
