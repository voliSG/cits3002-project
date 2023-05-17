from app.api.helpers import protected
from app.pages.helpers import load_template, replace_nth
import requests

MAX_ATTEMPTS = 3

MC_MAP = {
    "a": 1,
    "b": 2,
    "c": 3,
    "d": 4,
}

# mock data from user db
questions = [
    {
        "id": "0",
        "language": "python",
        "question": "What is the difference between a list and a tuple?\n a) Lists are immutable, tuples are mutable\n b) Lists are mutable, tuples are immutable\n c) Lists can store any data type while tuples are for integers only \n d) There is no difference\n",
        "type": "mc",
        "attempts": 1,
        "current_answer": "c",
        "correct": False,
    },
    {
        "id": "1",
        "language": "python",
        "question": "Write a program to print the first 10 numbers of the fibonacci sequence\n",
        "type": "code",
        "attempts": 1,
        "current_answer": "print('hello')",
        "correct": False,
    },
    {
        "id": "2",
        "language": "c",
        "question": "What is a pointer?\n a) A pointer is a variable that stores the address of another variable\n b) A pointer is a variable that stores the value of another variable\n c) A pointer is a variable that stores the address of a function\n d) A pointer is a variable that stores the value of a function\n",
        "type": "mc",
        "attempts": 3,
        "current_answer": "a",
        "correct": True,
    },
]

NUM_QUESTIONS_PER_QUIZ = 3


@protected
def GET_quiz(query, token=None):

    # URL endpoint of QB to fetch questions from
    url = "http://localhost:8001/api/getQuestions?numQs=" + \
        str(NUM_QUESTIONS_PER_QUIZ)
    # Send GET request
    response = requests.get(url)
    data = None
    # Check the response status code
    if response.status_code == 200:  # Successful response
        data = response.json()  # Parse response as JSON
        # You can now access the data using the same syntax as a Python dict, e.g data["questions"] <-- try printing that, you'll get what I mean.
    else:
        print("Request failed with status code:", response.status_code)

    status = 200
    template = load_template("quiz.html")

    questions_html = ""
    for i, q in enumerate(questions):
        # the question and answer template
        qa_html = ""

        if q["type"] == "mc":
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
        if q["type"] == "mc":
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

    headers = {}
    return status, template, headers
