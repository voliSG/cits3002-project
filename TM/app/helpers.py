from . import users


def check_login(username, password):
    if None in (username, password):
        status = 400
    else:
        found_user = next(
            (user for user in users if user["username"] == username), None
        )
        if found_user["password"] != password:
            status = 401
        else:
            status = 200
    return status
