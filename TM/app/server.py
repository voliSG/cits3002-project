import os
import pathlib
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

from app.routes import routes


class TMServer(Thread):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.ws = HTTPServer((self.host, self.port), TMHandler)

    def run(self):
        print(f"Server started on http://{self.host}:{self.port}")
        self.ws.serve_forever()

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
        self.join()


class TMHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        code = 500

        template_path = routes.get(self.path)

        if template_path is None:
            template_path = routes.get("404")
            code = 404

        template = self.__load_template(template_path)
        self.__send_response(code, template)

    def __load_template(self, path):
        try:
            full_path = os.path.join(pathlib.Path(__file__).parent.resolve(), path)
            f = open(full_path, "r")
            content = f.read()
        except Exception as e:
            print(e)
            content = "Error 500: Internal Server Error"
        return content

    def __send_response(self, code, body):
        self.send_response(code)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write(bytes(body, "utf-8"))
