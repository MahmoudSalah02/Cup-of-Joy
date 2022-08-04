"""
This is the employees module and supports all the REST actions for the
Employee table
"""

from models.models import Employee
import init_db
from models.schemas import EmployeeSchema


def read_all():
    """
    This function responds to a request for /api/employees
    with the complete lists of employees
    :return:        json string of list of employees
    """
    # Create the list of employees from our data
    session = init_db.get_session()
    employees = session.query(Employee).order_by(Employee.name).all()

    # Serialize the data for the response
    employee_schema = EmployeeSchema(many=True, session=session)
    employee_data = employee_schema.dump(employees)

    return employee_data, 200


def create(body):
    """
    This function creates a new employee based on the employee
    data passed in
    :param body: employee to be created
    :return: employee created if request successful, error 409 otherwise
    """
    session = init_db.get_session()
    existing_employee = (
        session.query(Employee).filter(Employee.contact_number == body.get("contact_number"))
        .one_or_none()
    )

    # if employee does not exist in the database
    if existing_employee is None:

        # deserialize employee to a database object
        employee_schema = EmployeeSchema()
        new_employee_deserialized = employee_schema.load(body, session=session)

        # add the employee to the database
        session.add(new_employee_deserialized)
        session.commit()

        employee_data = employee_schema.dump(new_employee_deserialized)
        return employee_data, 200

    # otherwise, person exists already
    else:
        return {"error": f"Employee {body.get('name')} already exists"}, 404


def read_one(employee_id):
    """
    This function responds to a request for /api/employees/{employee_id}
    with one matching employee from the database
    :param employee_id: id of employee to find
    :return: JSON object of the employee matching the id
    """
    session = init_db.get_session()
    existing_employee = (
        session.query(Employee).filter(Employee.id == employee_id)
        .one_or_none()
    )

    if existing_employee is not None:
        employee_schema = EmployeeSchema()
        employee_data_serialized = employee_schema.dump(existing_employee)
        return employee_data_serialized, 200

    else:
        return {"error": f"Employee not found for id: {employee_id}"}, 404


def update(employee_id, body):
    """
    This function updates an existing employee in the database
    :param employee_id: id of employee to update
    :param body: JSON object containing new changes to the employee
    :return: JSON object of the employee updated
    """
    session = init_db.get_session()
    read_one_response = read_one(employee_id)
    if read_one_response[1] == 404:
        return read_one_response

    # deserialize data into a database object
    employee_schema = EmployeeSchema()
    existing_employee_deserialized = employee_schema.load(body, session=session)

    session.merge(existing_employee_deserialized)
    session.commit()

    body["id"] = employee_id
    return body, 200


def delete(employee_id):
    """
    This function deletes an existing employee in the database
    :param employee_id: id of the employee to be deleted
    :return: JSON object of the employee deleted
    """
    session = init_db.get_session()
    existing_employee = read_one(employee_id)
    if existing_employee[1] == 404:
        return existing_employee

    # deserialize employee to a database object
    employee_schema = EmployeeSchema()
    employee_schema_deserialized = employee_schema.load(existing_employee[0], session=session)

    # if the execution reaches this line, then existing employee is not None
    session.delete(employee_schema_deserialized)
    session.commit()
    return existing_employee[0], 200
