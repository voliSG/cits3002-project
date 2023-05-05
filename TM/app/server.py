import os
import pathlib
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from urllib.parse import urlparse

from app.routes import api_folder, api_routes, page_routes


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

            api_action = api_route.get("GET")

            if api_action is None:
                status = 501
                self.__set_response(
                    status,
                    '{ "message": "Error 501: Not Implemented" }',
                    {"Content-Type": "application/json"},
                )
                return

            (status, content) = api_action(query)
            self.__set_response(
                status,
                content,
                {"Content-Type": "application/json"},
            )

        # handle pages
        else:
            template_path = page_routes.get(path)

            if template_path is None:
                template_path = page_routes.get("404")
                status = 404
            else:
                status = 200

            template = self.__load_template(template_path)
            self.__set_response(status, template, {"Content-Type": "text/html"})

    def do_POST(self):
        status = 500

        parsed_path = urlparse(self.path)
        query = parsed_path.query
        path = parsed_path.path
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)

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

        (status, content) = api_action(query, post_data)

        self.__set_response(status, content, {"Content-Type": "application/json"})

    def __load_template(self, path):
        try:
            full_path = os.path.join(pathlib.Path(__file__).parent.resolve(), path)
            f = open(full_path, "r")
            content = f.read()
        except Exception as e:
            print(e)
            content = "Error 500: Internal Server Error"
        return content

    def __set_response(self, code, body, headers):
        self.send_response(code)

        if headers:
            for header in headers:
                self.send_header(header, headers[header])
        self.end_headers()

        self.wfile.write(bytes(body, "utf-8"))
