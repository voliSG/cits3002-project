import os
import re
import random

from app.config import template_folder


def load_template(template_file):
    full_path = os.path.join(
        "app",
        "pages",
        template_folder,
        template_file,
    )

    f = open(full_path, "r")
    template = f.read()

    return template


def replace_nth(string, sub, wanted, n):
    if n == -1:
        return string
    where = [m.start() for m in re.finditer(sub, string)][n - 1]
    before = string[:where]
    after = string[where:]
    after = after.replace(sub, wanted, 1)
    newString = before + after
    return newString


def get_question_distribution(num_questions):
    num_python = random.randint(0, num_questions)
    num_c = num_questions - num_python

    return num_python, num_c
