"""
This is the employees module and supports all the REST actions for the
Employee table
"""

from flask import abort, make_response
from models.models import Employee, session
from models.schemas import EmployeeSchema


def read_all():
    """
    This function responds to a request for /api/employees
    with the complete lists of employees
    :return:        json string of list of employees
    """
    # Create the list of employees from our data
    employees = session.query(Employee).order_by(Employee.name).all()

    # Serialize the data for the response
    employee_schema = EmployeeSchema(many=True)
    employee_data = employee_schema.dump(employees)
    return employee_data


def create(body):
    """
    This function creates a new employee based on the employee
    data passed in
    :param body: employee to be created
    :return: employee created if request successful, error 409 otherwise
    """
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
        return employee_data, 201

    # otherwise, person exists already
    else:
        abort(409, f"Employee {body.get('name')} exists already")


def read_one(employee_id):
    """
    This function responds to a request for /api/employees/{employee_id}
    with one matching employee from the database
    :param employee_id: id of employee to find
    :return: employee matching the id
    """
    existing_employee = (
        session.query(Employee).filter(Employee.id == employee_id)
        .one_or_none()
    )

    if existing_employee is not None:
        employee_schema = EmployeeSchema()
        employee_data_serialized = employee_schema.dump(existing_employee)
        return employee_data_serialized

    else:
        abort(404, f"Employee not found for Id: {employee_id}")


def update(employee_id, body):
    """
    This function updates an existing employee in the database
    :param employee_id: id of employee to update
    :param employee: new changes to the employee
    :return:
    """

    existing_employee = read_one(employee_id)
    existing_employee["name"] = body.get("name")
    existing_employee["contact_number"] = body.get("contact_number")
    existing_employee["email"] = body.get("email")

    # deserialize data into a database object
    employee_schema = EmployeeSchema()
    existing_employee_deserialized = employee_schema.load(existing_employee, session=session)

    session.merge(existing_employee_deserialized)
    session.commit()

    return existing_employee, 200


def delete(employee_id):
    """
    This function deletes an existing employee in the database
    :param employee_id: id of the employee to be deleted
    :return:
    """
    existing_employee = read_one(employee_id)

    # deserialize employee to a database object
    employee_schema = EmployeeSchema()
    employee_schema_deserialized = employee_schema.load(existing_employee, session=session)

    # if the execution reaches this line, then existing employee is not None
    session.delete(employee_schema_deserialized)
    session.commit()
    return make_response(f"Employee {employee_id} deleted", 200)
