from app.pages.helpers import load_template


def GET_login(query, token=None):
    status = 200
    template = load_template("login.html")
    headers = {}
    return status, template, headers
