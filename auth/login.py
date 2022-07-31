from models.models import session, Employee
from models.schemas import EmployeeSchema


def process_registration_request(body):
    """

    :param body:
    :return:
    """

    # check if username exists in employee table
    if Employee.find_by_username(body.get("username")):
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

    # create a new access token for the newly registered employee
    access_token = new_employee_deserialized.encode_access_token()

    # TODO: should I commit changes in the end?
    session.commit()
    return {
        "access_token": Employee.decode_access_token(access_token).get("access_token"),
        "message": "successfully registered",
    }


def process_login_request(body):
    """

    :param body:
    :return:
    """

    # find the employee instance in the db
    existing_employee = Employee.find_by_username(body.get("username"))

    # return an error if username is not found or password is incorrect, otherwise, login
    if not existing_employee or not existing_employee.check_password(body.get("password")):
        return {
            "error": "password or username incorrect"
        }

    # generate new access token
    access_token = existing_employee.encode_access_token()
    return {
        "access_token": access_token,
        "message": "successfully logged in",
    }
