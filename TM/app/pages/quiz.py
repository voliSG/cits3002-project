from app.api.helpers import protected, decode_token
from app.pages.helpers import *
from http.cookies import SimpleCookie
from app import users
import urllib.request
import json


MAX_ATTEMPTS = 3

MC_MAP = {
    "a": 1,
    "b": 2,
    "c": 3,
    "d": 4,
}

# mock data from user db
# questions = [
#     {
#         "id": "0",
#         "language": "python",
#         "question": "What is the difference between a list and a tuple?\n a) Lists are immutable, tuples are mutable\n b) Lists are mutable, tuples are immutable\n c) Lists can store any data type while tuples are for integers only \n d) There is no difference\n",
#         "type": "mc",
#         "attempts": 1,
#         "current_answer": "c",
#         "correct": False,
#     },
#     {
#         "id": "1",
#         "language": "python",
#         "question": "Write a program to print the first 10 numbers of the fibonacci sequence\n",
#         "type": "code",
#         "attempts": 1,
#         "current_answer": "print('hello')",
#         "correct": False,
#     },
#     {
#         "id": "2",
#         "language": "c",
#         "question": "What is a pointer?\n a) A pointer is a variable that stores the address of another variable\n b) A pointer is a variable that stores the value of another variable\n c) A pointer is a variable that stores the address of a function\n d) A pointer is a variable that stores the value of a function\n",
#         "type": "mc",
#         "attempts": 3,
#         "current_answer": "a",
#         "correct": True,
#     },
# ]

# Questions fetched from QB will be stored in this dictionary, with the username of the user as the key
questions = {}

NUM_QUESTIONS_PER_QUIZ = 4
ADDRESS_FOR_PYTHON_QB = "http://localhost:8001"
ADDRESS_FOR_C_QB = "http://localhost:8002"


# def fetch_questions(url, num_questions):

#     # URL endpoint of QB to fetch questions from
#     # append number of questions as param
#     url += str(num_questions)
#     # Send GET request
#     response = requests.get(url)
#     data = None
#     # Check the response status code
#     if response.status_code == 200:  # Successful response
#         data = response.json()  # Parse response as JSON
#         print("Fetched a length of : " +
#               str(len(data['questions'])) + " questions!")
#         # You can now access the data using the same syntax as a Python dict, e.g data["questions"] <-- try printing that, you'll get what I mean.
#     else:
#         print("Request failed with status code:", response.status_code)

#     return data['questions']

#


def fetch_questions(url, num_questions):
    # URL endpoint of QB to fetch questions from
    # append number of questions as param
    url += str(num_questions)
    # Create a request object with the URL
    request = urllib.request.Request(url)

    try:
        # Send the request and get the response
        response = urllib.request.urlopen(request)

        # Read the response content
        data = response.read()

        # Assuming the response data is in JSON format
        # You can parse and process the data here
        # For example:
        questionData = json.loads(data)

        # Print the questions
        for question in questionData:
            print(question)

        return questionData['questions']

    except urllib.error.URLError as e:
        print("An error occurred:", e)


def updateQuestionsSchema(questions):
    for question in questions:
        question['attempts'] = 0
        question['correct'] = False

    return questions


@protected
def GET_quiz(query, token=None):

    # # get auth token from cookie
    # cookies = SimpleCookie(self.headers.get("Cookie"))
    # token_cookie = cookies.get("token")
    # token = token_cookie.value if token_cookie is not None else None

    username = decode_token(token)[0]

    if username not in questions.keys():
        # # randomise question distribution
        num_python, num_c = get_question_distribution(NUM_QUESTIONS_PER_QUIZ)

        # # fetch questions
        questions_py = fetch_questions(
            ADDRESS_FOR_PYTHON_QB + "/api/getQuestions?numQs=", num_python)
        questions_c = fetch_questions(
            ADDRESS_FOR_C_QB + "/api/getQuestions?numQs=", num_c)
        updateQuestionsSchema(questions_py)
        updateQuestionsSchema(questions_c)
        questions[username] = questions_py + questions_c

    print("Voila! Here are the questions: ")
    print(questions[username])

    # # save questions to user db
    # # python questions will always be before c questions

    # generate html from questions list in users
    template = load_template("quiz.html")

    questions_html = ""
    for i, q in enumerate(questions[username]):
        # the question and answer template
        qa_html = ""

        if q["id"] == 0 or q["id"] == 1:
            # dynamically load so we don't have to restart the server every time we decide to change the template
            qa_html = load_template("quiz-mc.html")
        else:
            qa_html = load_template("quiz-code.html")

        # 🔥🔥🔥 blazingly fast 🔥🔥🔥

        # the question string
        q_html = q["question"].replace("\n", "<br />")
        q_html = q["question"].replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")

        qa_html = qa_html.replace("{%QUESTION%}", q_html)
        qa_html = qa_html.replace("{%ID%}", str(q["id"]))
        qa_html = qa_html.replace(
            "{%ATTEMPTS%}", f"{q['attempts']}/{MAX_ATTEMPTS}")

        # check or fill in their latest answer
        if q["id"] == 0 or q["id"] == 1:
            qa_html = replace_nth(
                qa_html,
                "{%CHECKED%}",
                "checked",
                MC_MAP.get(q.get("current_answer"), -1),
            )
        else:
            qa_html = qa_html.replace(
                "{%CURRENT_ANSWER%}", q.get("current_answer", ""))

        # if correct, disable the question and colour it green
        if q["correct"]:
            qa_html = qa_html.replace("{%CORRECT%}", "bg-green-300")
            qa_html = qa_html.replace("{%DISABLED%}", "disabled")
            qa_html = qa_html.replace("{%ANSWER%}", "")
        else:
            # if they've used up all their attempts, disable the question
            if q["attempts"] >= MAX_ATTEMPTS:
                qa_html = qa_html.replace("{%CORRECT%}", "bg-red-400")
                qa_html = qa_html.replace("{%DISABLED%}", "disabled")
                # TODO fetch the correct answer from the db
                qa_html = qa_html.replace("{%ANSWER%}", "THE ANSWER")
            else:
                # cleanup
                qa_html = qa_html.replace("{%CORRECT%}", "")
                qa_html = qa_html.replace("{%DISABLED%}", "")
                qa_html = qa_html.replace("{%ANSWER%}", "")

        questions_html += qa_html

    template = template.replace("{%QUESTIONS%}", questions_html)
    status = 200
    headers = {}
    return status, template, headers


if __name__ == "__main__":
    pass
