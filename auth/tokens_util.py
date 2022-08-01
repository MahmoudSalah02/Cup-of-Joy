from jwt import encode, decode
from datetime import timedelta, datetime
from config.config import PRIVATE_KEY_PATH, PUBLIC_KEY_PATH, ALGORITHM

# TODO: error when you this file is imported from inside /seeds/
PRIVATE_KEY = open(PRIVATE_KEY_PATH).read()
PUBLIC_KEY = open(PUBLIC_KEY_PATH).read()


def encode_access_token(employee):
    """
    This function creates and returns an encoded access token
    :return: string representing an encoded access token
    """
    payload = {
        'exp': datetime.utcnow() + timedelta(days=1),
        "iat": datetime.utcnow(),
        "sub": employee.id,
        "username": employee.username,
        "role": employee.role,
    }
    return encode(payload, PRIVATE_KEY, algorithm=ALGORITHM)


def decode_access_token(access_token):
    """

    :param access_token:
    :return:
    """
    return decode(access_token, PUBLIC_KEY, algorithms=ALGORITHM)
