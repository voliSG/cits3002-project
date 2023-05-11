from app.pages.helpers import load_template


def GET_404(query, token=None):
    status = 404
    template = load_template("404.html")
    headers = {}
    return status, template, headers
