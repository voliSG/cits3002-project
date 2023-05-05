import json


def POST_login(query, body):
    status = 200
    response = {"message": "Login successful.", "token": "123"}
    return status, json.dumps(response)
