import os

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
