from flask import request
from project.config import config
from project.auth import tokens_util

def validate_token():
    """
    This function validates an access token and checks
    roles and permissions accordingly
    :return:
    """
    # check if the API endpoint exists
    path_rule = getattr(request.url_rule or {}, "rule", None)
    if path_rule not in config.ROLE_MAPPING.keys():
        raise Exception("API endpoint not found")

    # user does not need a token to register or login
    # coding wise, check if api endpoint roles are None
    if not config.ROLE_MAPPING.get(path_rule):
        return None

    # At this point, the user must have access token
    authorization_header = request.headers.get("Authorization", None)
    if not authorization_header:
        raise Exception("Access Token not found")

    # note that if access token is empty, the word Bearer will not be passed to headers
    # at this point, the authorization_header looks something like: "Bearer ___access_token____"
    # thus we will parse and return "___access_token____"
    access_token_parsed = authorization_header.split("Bearer")[1].strip()
    access_token_decoded = tokens_util.decode_access_token(access_token_parsed)

    is_allowed = check_permission(path_rule, access_token_decoded)
    if not is_allowed:
        raise Exception("Employee not Authorized")


def check_permission(path, token):
    """
    This method checks if an employee with access token is allowed
    to access a particular resource
    :param path: API endpoint the employee is trying to access
    :param token: Decoded access token of the employee
    :return: Boolean value of whether the employee is allowed access to the resource
    """
    role = token.get("role")
    return role in config.ROLE_MAPPING.get(path)
