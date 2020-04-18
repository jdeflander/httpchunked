from http import HTTPStatus
from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler, HTTPServer
from io import BytesIO
from threading import Thread
from unittest import TestCase

from httpchunked import decode, encode


class TestHTTPChunked(TestCase):
    _connection: HTTPConnection
    _server: HTTPServer
    _thread: Thread

    @classmethod
    def setUpClass(cls) -> None:
        server_address = "", 0
        cls._server = HTTPServer(server_address, _Handler)
        cls._thread = Thread(target=cls._server.serve_forever)
        cls._thread.start()
        cls._connection = HTTPConnection("localhost", cls._server.server_port)

    def test_decode(self):
        body = [b"foo", b"bar", b"baz"]
        self._connection.request("POST", "/decode", body=body)
        response = self._connection.getresponse()

        expected = b"".join(body)
        actual = response.read()
        self.assertEqual(expected, actual)

    def test_encode(self):
        body = b"foo"
        headers = {"Accept-Encoding": "chunked"}
        self._connection.request("POST", "/encode", body=body, headers=headers)
        response = self._connection.getresponse()

        expected = body
        actual = response.read()
        self.assertEqual(expected, actual)

    @classmethod
    def tearDownClass(cls) -> None:
        cls._connection.close()
        cls._server.shutdown()
        cls._server.server_close()
        cls._thread.join()


class _Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def do_POST(self):
        if self.path == "/decode":
            self.send_response(HTTPStatus.OK)
            buf = BytesIO()
            decode(buf, self.rfile)
            raw = buf.getvalue()
            content_length = len(raw)
            self.send_header("Content-Length", content_length)
            self.end_headers()
            self.wfile.write(raw)

        elif self.path == "/encode":
            self.send_response(HTTPStatus.OK)
            self.send_header("Transfer-Encoding", "chunked")
            self.end_headers()
            content_length_str = self.headers["Content-Length"]
            content_length = int(content_length_str)
            raw = self.rfile.read(content_length)
            buf = BytesIO(raw)
            encode(self.wfile, buf)

        else:
            self.send_error(HTTPStatus.NOT_FOUND)

    def log_message(self, format_, *args):
        pass
