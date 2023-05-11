import re

from app.api.helpers import protected
from app.pages.helpers import load_template

questions = [
    'What is the difference between a list and a tuple?\n a) Lists are immutable, tuples are mutable\n b) Lists are mutable, tuples are immutable\n c) Lists can store any data type while tuples are for integers only \n d) There is no difference\n'
]

# @protected
def GET_quiz(query, token=None):
    status = 200
    template = load_template("quiz.html")
    
    parsed = re.sub(r"/(?:\r\n|\r|\n)/g", '<br />', questions[0])
    print(parsed)
    headers = {}
    return status, template, headers
