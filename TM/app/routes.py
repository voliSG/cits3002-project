import app.api as api
from app import pages
from app.config import api_folder

page_routes = {
    "404": pages.not_found.GET_404,
    "/": pages.home.GET_home,
    "/login": pages.login.GET_login,
}

api_routes = {
    f"/{api_folder}/login": {
        "POST": api.login.POST_login,
    },
    f"/{api_folder}/test": {
        "GET": api.test.GET_questions,
    },
    f"/{api_folder}/answer": {
        "GET": api.test.POST_answer,
    },
}
