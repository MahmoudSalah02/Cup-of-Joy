from models.models import Employee
from init_db import session
from models.schemas import EmployeeSchema
from auth.tokens_util import create_access_token


def process_registration_request(body):
    """

    :param body:
    :return:
    """
    # check if username exists in employee table
    if find_by_username(body.get("username")):
        return {"error": f"{body.get('username')} already exists"}

    # gather employee info in a dictionary
    employee_info = {
        "name": body.get("name"),
        "contact_number": body.get("contact_number"),
        "email": body.get("email"),
        "role": body.get("role")
    }

    # deserialize employee info JSON into a db object
    employee_schema = EmployeeSchema()
    new_employee_deserialized = employee_schema.load(employee_info, session=session)

    # add the object in the db and commit changes
    session.add(new_employee_deserialized)
    new_employee_deserialized.set_username(body.get("username"))
    new_employee_deserialized.set_hash_password(body.get("password"))

    session.commit()

    return employee_schema.dump(new_employee_deserialized)


def process_login_request(body):
    """

    :param body:
    :return:
    """

    # find the employee instance in the db
    existing_employee = find_by_username(body.get("username"))

    # return an error if username is not found or password is incorrect, otherwise, login
    if not existing_employee or not existing_employee.check_password(body.get("password")):
        return {"error": "password or username incorrect"}

    # generate new access token
    return {"access_token": create_access_token(existing_employee)}


def find_by_username(username):
    """
    This function finds the user with a matching username
    :param username: username of the user to find
    :return: user with matching username
    """
    return session.query(Employee).filter(Employee.username == username).one_or_none()
