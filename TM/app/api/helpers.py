import base64

from app import users


def find(list, key, value):
    for i, dic in enumerate(list):
        if dic[key] == value:
            return i
    return -1


def decode_token(token):
    """
    Converts a base64 encoded token into a username and password which should be in the format username:password
    """

    if token is None or token == "":
        return None, None
    (username, password) = base64.b64decode(token).decode("utf-8").split(":")
    return username, password


def is_new_login(user):
    """
    Checks if the user is logging in for the first time
    """
    return len(user.get("questions")) == 0


def check_login(username, password):
    """
    Checks the username and password against the users dictionary
    """

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
            print(found_user)
            is_new = is_new_login(found_user)
    return status, is_new


def protected(func):
    """
    An awesome decorator that makes the function (endpoint) return early with
    the error if the user does not provide their auth cookie in the request
    """

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

        if status == 200:
            pass
        elif status == 401:
            template = "Error 401: Unauthorized"
            headers = {"WWW-Authenticate": "Basic"}
            return status, template, headers
        elif status == 400:
            template = "Error 400: Bad Request"
            return status, template, headers

        return func(*args, **kwargs, username=username)

    return wrapper_protected
