import base64
import os
import pathlib

from .. import users


def decode_token(token):
    if token is None:
        return None, None
    (username, password) = base64.b64decode(token).decode("utf-8").split(":")
    return username, password


def check_login(username, password):
    if None in (username, password):
        status = 400
    else:
        found_user = next(
            (user for user in users if user["username"] == username), None
        )
        if found_user.get("password") != password:
            status = 401
        else:
            status = 200
    return status


def protected(func):
    def wrapper_protected(*args, **kwargs):
        status = 500
        template = "Error 500: Internal Server Error"
        headers = {}

        (username, password) = decode_token(kwargs.get("token"))

        if username is None or password is None:
            status = 401
            template = "Error 401: Unauthorized"
            return status, template, headers

        status = check_login(username, password)

        match status:
            case 200:
                pass
            case 401:
                template = "Error 401: Unauthorized"
                headers = {"WWW-Authenticate": "Basic"}
                return status, template, headers
            case 400:
                template = "Error 400: Bad Request"
                return status, template, headers

        return func(args)

    return wrapper_protected
