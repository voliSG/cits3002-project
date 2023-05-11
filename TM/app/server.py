import json
from http.cookies import SimpleCookie
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
        """
        GET Requests
        """

        status = 500

        parsed_path = urlparse(self.path)
        query = parsed_path.query
        path = parsed_path.path

        # get auth token from cookie
        cookies = SimpleCookie(self.headers.get("Cookie"))
        token_cookie = cookies.get("token")
        token = token_cookie.value if token_cookie is not None else None

        # handle api endpoints
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

            action = api_route.get("GET")

            if action is None:
                status = 501
                self.__set_response(
                    status,
                    '{ "message": "Error 501: Not Implemented" }',
                    {"Content-Type": "application/json"},
                )
                return

            (status, content, headers) = action(query, token=token)
            self.__set_response(
                status,
                content,
                {"Content-Type": "application/json", **headers},
            )

        # handle pages
        else:
            action = page_routes.get(path)

            if action is None:
                action = page_routes.get("404")

            status, template, headers = action(query, token=token)

            self.__set_response(status, template, {"Content-Type": "text/html"})

    def do_POST(self):
        """
        POST Requests
            We assume all requests are JSON with JSON responses for simplicity
        """

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

    def __set_response(self, code, body, headers):
        """
        Set the response for the request
        """
        self.send_response(code)

        if headers:
            for header in headers:
                self.send_header(header, headers[header])
        self.end_headers()

        self.wfile.write(bytes(body, "utf-8"))
