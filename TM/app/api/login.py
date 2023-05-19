import base64
import json
import random
import colorama
from colorama import Fore
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
        questionData = json.loads(data)

        # Code to print the questions! (For testing purposes. Uncomment if needed.)
        # print(Fore.GREEN + "\nHere\'s the questions yo boi shall face" + Fore.YELLOW)
        # for question in questionData['questions']:
        #     print("\tQ: " + question['question'].replace("\n", "\n  \t"))
        # print(Fore.WHITE)

        if 'questions' not in questionData.keys():
            return []
        return questionData["questions"]

    except json.JSONDecodeError:
        # all python or all c questions
        return []
    except URLError as e:
        print(
            Fore.RED + "An error occurred while connecting to " + Fore.YELLOW + url + Fore.RED + " :\n", e.reason, Fore.WHITE)


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
            print(
                Fore.GREEN + "[TM] Voila! A new user has logged in for the first time!" + Fore.WHITE)

            # randomise question distribution
            num_python, num_c = get_question_distribution(
                NUM_QUESTIONS_PER_QUIZ)

            # fetch questions
            questions_py = fetch_questions(
                qb_python + "/api/getQuestions?numQs=", num_python
            )
            questions_c = fetch_questions(qb_c + "/api/getQuestions?numQs=", num_c)

            updateQuestionsSchema(questions_py, Language.PYTHON)
            updateQuestionsSchema(questions_c, Language.C)
            print(Fore.GREEN + "[TM] Questions have been fetched from the question bank! Fetched " + Fore.YELLOW + str(num_c) +
                  Fore.GREEN + " C questions and " + Fore.YELLOW + str(num_python) + Fore.GREEN + " Python questions." + Fore.WHITE)

            user = next(u for u in users if u["username"] == username)

            user["questions"] = questions_py + questions_c

    elif status == 401:
        response = {"message": "Invalid username or password."}

    return status, json.dumps(response), headers
