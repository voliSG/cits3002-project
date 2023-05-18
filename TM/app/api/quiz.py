import json

from urllib.parse import urlencode
from urllib.request import Request, urlopen

from app import users
from app.api.helpers import protected, find
from app.config import qb_python, qb_c
from app.pages.quiz import MAX_ATTEMPTS


@protected
def GET_questions(query, username, **kwargs):
    status = 200
    response = [{"question": "What is your name?"}, {"question": "What is your quest?"}]
    return status, json.dumps(response)


def POST_answer(query, body, **kwargs):
    status = 200
    q_id = body.get("qId")
    answer = body.get("answer")

    # ! this is broken and i don't know how to fix it
    username = kwargs.get("username", "123")

    # do it this dumb way just in case it's not passing by reference
    user_index = find(users, "username", username)

    if user_index == -1:
        status = 400
        response = {"error": "User not found. Somehow..."}
        return status, json.dumps(response), {}

    question_index = find(users[user_index]["questions"], "id", q_id)

    if question_index == -1:
        status = 400
        response = {"error": "Question not found."}
        return status, json.dumps(response), {}

    question = users[user_index]["questions"][question_index]

    if question["attempts"] >= MAX_ATTEMPTS:
        status = 400
        response = {"error": "You have exceeded the maximum number of attempts."}
        return status, json.dumps(response), {}

    qb = ""

    if question["language"] == "python":
        qb = qb_python
    elif question["language"] == "c":
        qb = qb_c

    data = urlencode({"qId": q_id, "answer": answer}).encode()

    req = Request(
        f"{qb}/api/questions/check",
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    res = urlopen(req).read().decode()

    question["attempts"] += 1
    question["correct"] = res == "true"
    question["current_answer"] = answer

    if res == "false":
        response = {"correct": False}
    else:
        response = {"correct": True}

    return status, json.dumps(response), {}
