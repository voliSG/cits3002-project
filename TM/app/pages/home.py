from app.api.helpers import protected
from app.pages.helpers import load_template


@protected
def GET_home(query, token=None):
    status = 200
    template = load_template("index.html")
    headers = {}
    return status, template, headers
