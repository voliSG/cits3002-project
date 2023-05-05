import app.api as api

template_folder = "templates"
api_folder = "api"

page_routes = {
    "404": f"{template_folder}/404.html",
    "/": f"{template_folder}/index.html",
    "/login": f"{template_folder}/login.html",
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
