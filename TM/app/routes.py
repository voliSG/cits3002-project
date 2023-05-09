import app.api as api

template_folder = "templates"
api_folder = "api"

page_routes = {
    "404": {"path": f"{template_folder}/404.html", "protected": False},
    "/": {"path": f"{template_folder}/index.html", "protected": True},
    "/login": {"path": f"{template_folder}/login.html", "protected": False},
}

api_routes = {
    f"/{api_folder}/login": {
        "POST": {"action": api.login.POST_login, "protected": False},
    },
    f"/{api_folder}/test": {
        "GET": {"action": api.test.GET_questions, "protected": True},
    },
    f"/{api_folder}/answer": {
        "GET": {"action": api.test.POST_answer, "protected": True},
    },
}
