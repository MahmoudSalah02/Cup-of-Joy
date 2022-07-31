from flask import request
from models.models import Employee
from config.config import ROLE_MAPPING


def validate_token():
    """
    This function validates an access token and checks
    roles and permissions accordingly

    TODO: what does it return? exceptions? None?
    :return:
    """
    # Authorization header is not required for login and registration
    if is_login_endpoint(request.url):
        return None

    # get, parse, and decode the authorization header
    authorization_header = request.headers.get("Authorization", None)
    access_token = parse_token(authorization_header)
    access_token_decoded = Employee.decode_access_token(access_token)

    if not access_token_decoded:
        return {"error": "token can't be parsed"}
    else:
        is_allowed = check_roles(request.url, access_token_decoded.get("role"))
        if is_allowed:
            return None
        else:
            return {"error": "user not allowed (roles)"}


def check_roles(request_url, role):
    """
    This function checks the role of an employee to see if the employee can access a particular resource
    :param request_url: string representing the URL the employee tried to access
    :param role: string representing the role of the employee, example: admin, cashier
    :return: boolean value of whether the employee is allowed to access a particular resource
    """
    if "/shop" in request_url:
        return role in ROLE_MAPPING.get("/shop")

    elif "/operation" in request_url:
        return role in ROLE_MAPPING.get("/operation")

    # TODO: return an exception? or just false?
    return False


def is_login_endpoint(url):
    """
    This function checks if a URL belongs to a login URL (/login, /register)
    :param url: string representing the URL
    :return: true of the URL is a (/login, /register), false otherwise
    """
    return "/login" in url or "/register" in url


def parse_token(authorization_header):
    """
    This function takes the authorization header, parses it, and
    returns the access token
    :param authorization_header:
    :return: string representing the access token
    """
    if not authorization_header:
        return {
            "error": "Authorization header missing",
            "status code": 401,
        }

    if str(authorization_header).startswith("Bearer "):
        split = authorization_header.split("Bearer")
        access_token = split[1].strip()
        return access_token
