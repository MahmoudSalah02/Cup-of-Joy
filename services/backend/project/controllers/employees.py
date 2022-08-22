"""
This is the employees module and supports all the REST actions for the
Employee table
"""

from project import init_db
from project.models import models, schemas

def read_all():
    """
    This function responds to a request for /api/employees
    with the complete lists of employees
    :return:        json string of list of employees
    """
    # Create the list of employees from our data
    session = init_db.get_session()
    employees = session.query(models.Employee).order_by(models.Employee.name).all()

    # Serialize the data for the response
    employee_schema = schemas.EmployeeSchema(many=True, session=session)
    employee_data = employee_schema.dump(employees)

    return employee_data, 200


def read_one(employee_id):
    """
    This function responds to a request for /api/employees/{employee_id}
    with one matching employee from the database
    :param employee_id: id of employee to find
    :return: JSON object of the employee matching the id
    """
    session = init_db.get_session()
    existing_employee = (
        session.query(models.Employee).filter(models.Employee.id == employee_id)
        .one_or_none()
    )

    if existing_employee is not None:
        employee_schema = schemas.EmployeeSchema()
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
    employee_schema = schemas.EmployeeSchema()
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
    employee_schema = schemas.EmployeeSchema()
    employee_schema_deserialized = employee_schema.load(existing_employee[0], session=session)

    # if the execution reaches this line, then existing employee is not None
    session.delete(employee_schema_deserialized)
    session.commit()
    return existing_employee[0], 200
