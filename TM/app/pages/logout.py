from app.api.helpers import protected
from app.pages.helpers import load_template


def GET_logout(query, token=None):
    status = 200
    template = load_template("logout.html")
    headers = {}
    return status, template, headers
