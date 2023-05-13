import base64
import json

from app import users
from app.api.helpers import check_login


def POST_login(query, body):
    status = 500
    response = {"message": "Internal server error."}
    headers = {}

    username = body.get("username")
    password = body.get("password")

    status = check_login(username, password)

    if status == 200:
        auth_bytes = f"{username}:{password}".encode("ascii")
        token = base64.b64encode(auth_bytes).decode("ascii")
        response = {"message": "Login successful.", "token": token}
    elif status == 401:
        response = {"message": "Invalid username or password."}

    return status, json.dumps(response), headers
