from urllib.error import URLError
from urllib.request import Request, urlopen

from app import users
from app.api.helpers import protected
from app.config import qb_c, qb_python
from app.enums import Language
from app.pages.helpers import load_template, replace_nth

MAX_ATTEMPTS = 3

MC_MAP = {
    "a": 1,
    "b": 2,
    "c": 3,
    "d": 4,
}


# Fetches sample answer from QB endpoint
def fetch_sampleAnswer(url, qId):
    # append qid to url as param
    url += str(qId)
    # Create a request object with the URL
    request = Request(url)

    try:
        # Send the request and get the response
        response = urlopen(request)

        # Read the response content
        data = response.read()

        # Convert from byte stream to string
        data = data.decode("utf-8")

        return data

    except URLError as e:
        print("An error occurred:", e)


@protected
def GET_quiz(query, token=None, username=None):
    # generate html from questions list in users
    template = load_template("quiz.html")

    user = next(filter(lambda u: u["username"] == username, users), None)

    questions_html = ""
    for i, q in enumerate(user["questions"]):
        # the question and answer template
        qa_html = ""

        if q["type"] == "MC":
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
        qa_html = qa_html.replace("{%ATTEMPTS%}", f"{q['attempts']}/{MAX_ATTEMPTS}")

        # check or fill in their latest answer
        if q["id"] == 0 or q["id"] == 1:
            qa_html = replace_nth(
                qa_html,
                "{%CHECKED%}",
                "checked",
                MC_MAP.get(q.get("current_answer"), -1),
            )
        else:
            qa_html = qa_html.replace("{%CURRENT_ANSWER%}", q.get("current_answer", ""))

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
                if q["language"] == Language.PYTHON:
                    sample_answer = fetch_sampleAnswer(
                        qb_python + "/api/questions/sample?qId=", q["id"]
                    )
                else:
                    sample_answer = fetch_sampleAnswer(
                        qb_c + "/api/questions/sample?qId=", q["id"]
                    )

                qa_html = qa_html.replace("{%ANSWER%}", "Answer: " + sample_answer)
            else:
                # cleanup
                qa_html = qa_html.replace("{%CORRECT%}", "")
                qa_html = qa_html.replace("{%DISABLED%}", "")
                qa_html = qa_html.replace("{%ANSWER%}", "")

        questions_html += qa_html

    template = template.replace("{%QUESTIONS%}", questions_html)
    template = template.replace(
        "{%SCORE%}", f"{user['score']}/{len(user['questions']) * MAX_ATTEMPTS}"
    )

    print(template)
    status = 200
    headers = {}
    return status, template, headers


if __name__ == "__main__":
    pass
