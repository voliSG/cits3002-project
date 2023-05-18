import json

from urllib.parse import urlencode
from urllib.request import Request, urlopen

from app import users
from app.api.helpers import protected
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

    # * temp default
    username = kwargs.get("username", "123")

    user = next((user for user in users if user["username"] == username), None)

    print(user)
    if not user:
        status = 400
        response = {"error": "User not found. Somehow..."}
        return status, json.dumps(response), {}

    question = next(
        (question for question in user["questions"] if question["id"] == q_id), None
    )

    if not question:
        status = 400
        response = {"error": "Question not found."}
        return status, json.dumps(response), {}

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

    print(data)

    req = Request(
        f"{qb}/api/questions/check",
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    res = urlopen(req).read().decode()

    if res == "false":
        status = 400
        response = {"correct": False}
        return status, json.dumps(response), {}
    if user:
        user["attempts"] += 1

    response = {"correct": True}
    return status, json.dumps(response), {}
