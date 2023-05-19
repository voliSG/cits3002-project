import base64
import json
import random
from urllib.error import URLError
from urllib.request import Request, urlopen

from app import users
from app.api.helpers import check_login
from app.config import qb_c, qb_python
from app.enums import Language

NUM_QUESTIONS_PER_QUIZ = 4


def get_question_distribution(num_questions):
    num_python = random.randint(0, num_questions)
    num_c = num_questions - num_python

    return num_python, num_c


def fetch_questions(url, num_questions):
    # URL endpoint of QB to fetch questions from
    # append number of questions as param
    url += str(num_questions)
    # Create a request object with the URL
    request = Request(url)

    try:
        # Send the request and get the response
        response = urlopen(request)

        # Read the response content
        data = response.read()

        # Assuming the response data is in JSON format
        # You can parse and process the data here
        # For example:
        questionData = json.loads(data)

        # Print the questions
        for question in questionData:
            print(question)

        return questionData["questions"]

    except URLError as e:
        print("An error occurred:", e)


def updateQuestionsSchema(questions, language):
    for question in questions:
        question["attempts"] = 0
        question["correct"] = False
        question["current_answer"] = ""

        if language == Language.PYTHON:
            question["language"] = Language.PYTHON
        elif language == Language.C:
            question["language"] = Language.C

    return questions


def POST_login(query, body, **kwargs):
    status = 500
    response = {"message": "Internal server error."}
    headers = {}

    username = body.get("username")
    password = body.get("password")

    status, is_new = check_login(username, password)

    if status == 200:
        auth_bytes = f"{username}:{password}".encode("ascii")
        token = base64.b64encode(auth_bytes).decode("ascii")
        response = {"message": "Login successful.", "token": token}

        if not is_new:
            print("New login!")

            # randomise question distribution
            num_python, num_c = get_question_distribution(NUM_QUESTIONS_PER_QUIZ)

            # fetch questions
            questions_py = fetch_questions(
                qb_python + "/api/getQuestions?numQs=", num_python
            )
            questions_c = fetch_questions(qb_c + "/api/getQuestions?numQs=", num_c)

            updateQuestionsSchema(questions_py, Language.PYTHON)
            updateQuestionsSchema(questions_c, Language.C)

            user = next(u for u in users if u["username"] == username)

            user["questions"] = questions_py + questions_c

    elif status == 401:
        response = {"message": "Invalid username or password."}

    return status, json.dumps(response), headers
