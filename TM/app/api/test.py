import json

from app.api.helpers import protected


@protected
def GET_questions(query):
    status = 200
    response = [{"question": "What is your name?"}, {"question": "What is your quest?"}]
    return status, json.dumps(response)


@protected
def POST_answer(query, body):
    status = 200
    response = {"correct": True}
    return status, json.dumps(response)
