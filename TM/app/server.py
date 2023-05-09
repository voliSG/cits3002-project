import base64
import json
import os
import pathlib
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from urllib.parse import urlparse

from app.helpers import check_login
from app.routes import api_folder, api_routes, page_routes

from . import users


class TMServer(Thread):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.ws = HTTPServer((self.host, self.port), TMHandler)

    def run(self):
        print(f"Server started on http://{self.host}:{self.port}")
        self.ws.serve_forever()

    # this complicated shutdown is supposed to allow keyboard interrupts to work on Windows but they still don't...
    def shutdown(self):
        # set the two flags needed to shutdown the HTTP server manually
        self.ws._BaseServer__is_shut_down.set()
        self.ws.__shutdown_request = True

        print("Shutting down server.")
        # call it anyway, for good measure...
        self.ws.shutdown()
        print("Closing server.")
        self.ws.server_close()
        print("Closing thread.")
        self.join(3000)


class TMHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        status = 500

        parsed_path = urlparse(self.path)
        query = parsed_path.query
        path = parsed_path.path

        # handle api
        if path.startswith(f"/{api_folder}"):
            api_route = api_routes.get(path)

            if api_route is None:
                status = 404
                self.__set_response(
                    status,
                    '{ "message": "Error 404: Not Found" }',
                    {"Content-Type": "application/json"},
                )
                return

            route = api_route.get("GET")
            action = route["action"]
            protected = route["protected"]

            if action is None:
                status = 501
                self.__set_response(
                    status,
                    '{ "message": "Error 501: Not Implemented" }',
                    {"Content-Type": "application/json"},
                )
                return

            (status, content) = action(query)
            self.__set_response(
                status,
                content,
                {"Content-Type": "application/json"},
            )

        # handle pages
        else:
            template_route = page_routes.get(path)

            if template_route is None:
                template_route = page_routes.get("404")
                status = 404
            else:
                status = 200

            status, template = self.__load_template(template_route)
            self.__set_response(status, template, {"Content-Type": "text/html"})

    def do_POST(self):
        status = 500

        parsed_path = urlparse(self.path)
        query = parsed_path.query
        path = parsed_path.path

        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode("utf-8")
        payload = json.loads(post_data)

        api_route = api_routes.get(path)

        if api_route is None:
            status = 404
            self.__set_response(
                status,
                '{ "message": "Error 404: Not Found" }',
                {"Content-Type": "application/json"},
            )
            return

        api_action = api_route.get("POST")

        if api_action is None:
            status = 501
            self.__set_response(
                status,
                '{ "message": "Error 501: Not Implemented" }',
                {"Content-Type": "application/json"},
            )
            return

        (status, content, headers) = api_action(query, payload)

        self.__set_response(
            status, content, {"Content-Type": "application/json", **headers}
        )

    def __load_template(self, template_route):
        status = 500
        template = "Error 500: Internal Server Error"

        try:
            if template_route["protected"]:
                token = self.headers["Authorization"]

                (username, password) = self.__decode_token(token)

                if username is None or password is None:
                    status = 401
                    template = "Error 401: Unauthorized"
                    return status, template

                status = check_login(username, password)

                match status:
                    case 200:
                        pass
                    case 401:
                        self.send_header(
                            "WWW-Authenticate", 'Basic realm="Login Required"'
                        )
                        template = "Error 401: Unauthorized"
                    case 400:
                        template = "Error 400: Bad Request"
                    case _:
                        template = "Error 500: Internal Server Error"

            full_path = os.path.join(
                pathlib.Path(__file__).parent.resolve(),
                template_route["path"],
            )

            f = open(full_path, "r")
            template = f.read()
        except Exception as e:
            print(e)
        return status, template

    def __set_response(self, code, body, headers):
        self.send_response(code)

        if headers:
            for header in headers:
                self.send_header(header, headers[header])
        self.end_headers()

        self.wfile.write(bytes(body, "utf-8"))

    def __decode_token(self, token):
        if token is None:
            return None, None
        (username, password) = base64.b64decode(token).decode("utf-8").split(":")
        return username, password
