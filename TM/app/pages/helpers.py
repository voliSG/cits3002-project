import os
import random
import re

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
