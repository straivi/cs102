import asyncore
import asynchat
import socket
import multiprocessing
import logging
import os
import urllib
import argparse
from mimetypes import guess_type
from time import strftime
from datetime import datetime

def url_normalize(path):
    if path.startswith("/"):
        path = path[1:]
    if path.startswith("."):
        path = "/" + path
    while "../" in path:
        p1 = path.find("/..")
        p2 = path.rfind("/", 0, p1)
        if p2 != -1:
            path = path[:p2] + path[p1+3:]
        else:
            path = path.replace("/..", "", 1)
    path = path.replace("/./", "/")
    path = path.replace("/.", "")
    path = path.replace("%20", " ")
    if "?" in path:
        num = path.index("?")
        path = path[:num]
    return path

logging.basicConfig(
        level=logging.DEBUG,
        format='[%(levelname)s] %(message)s'
    )
log = logging

responses = {
    200: ('OK', 'Request fulfilled, document follows'),
    400: ('Bad Request',
        'Bad request syntax or unsupported method'),
    403: ('Forbidden',
        'Request forbidden -- authorization will not help'),
    404: ('Not Found', 'Nothing matches the given URI'),
    405: ('Method Not Allowed',
        'Specified method is invalid for this resource.'),
}

class FileProducer(object):

    def __init__(self, f, chunk_size=4096):
        self.file = f
        self.chunk_size = chunk_size

    def more(self):
        if self.file:
            data = self.file.read(self.chunk_size)
            if data:
                return data
            self.file = None
        return ""


class AsyncServer(asyncore.dispatcher):

    def __init__(self, host="127.0.0.1", port=9000):
        super().__init__()
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)


    def handle_accepted(self, sock, addr):
        log.debug(f"Incoming connection from {addr}")
        AsyncHTTPRequestHandler(sock)

    def serve_forever(self):
        asyncore.loop()


class AsyncHTTPRequestHandler(asynchat.async_chat):

    def __init__(self, sock):
        super().__init__(sock)
        self.data = ""
        self.request = None
        self.set_terminator(b"\r\n\r\n")
        self.shutdown = 0
        self.content_len = 0
        self.file_type = ""
        self.path = ""
        self.server_name = "localhost"
        self.port = 9000

    def collect_incoming_data(self, data):
        self.data = data.decode()
        log.debug(f"Incoming data: {self.data}")

    def found_terminator(self):
        self.parse_request()

    def parse_request(self):
        if not self.request:
            self.request = {}
            self.data_list = self.data.split('\r\n')
            
            self.parse_headers()    

            if not self.response_is_good:
                self.send_error(400, responses[400])
                self.shutdown = 1

        self.handle_request()

    def parse_headers(self):
        first_line_list = self.data_list[0].split()
        self.method = first_line_list[0]
        self.path = url_normalize(first_line_list[1])
        self.protocol = first_line_list[2]
        self.response_is_good = True

        self.info = self.data_list[1:]
        body_index = None

        for item in self.info:
            if item == '\r\n':
                body_index = self.data_list.index(item)
                break
            item_data = item.split(": ")
            if len(item_data) == 2:
                self.request[item_data[0]] = item_data[1]
            else:
                self.response_is_good == False
                break

        if body_index:
            self.body = '\n'.join(self.data_list[body_index + 1:])

    def handle_request(self):
        method_name = 'do_' + self.method
        if not hasattr(self, method_name):
            self.send_error(405)
            self.handle_close()
            return
        handler = getattr(self, method_name)
        handler()

    def send_header(self, keyword: str, value: str) -> None:
        self.push(f"{keyword}: {value}\r\n".encode())

    def send_error(self, code, message=None):
        try:
            short_msg, long_msg = responses[code]
        except KeyError:
            short_msg, long_msg = '???', '???'
        if message is None:
            message = short_msg
        self.send_response(code, message)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Connection", "Closed")
        self.end_headers()

    def send_response(self, code, message):
        self.push("HTTP/1.1 {} {}\r\n".format(code, message).encode())

    def end_headers(self):
        self.push("\r\n".encode())

    @staticmethod
    def date_time_string():
        now = datetime.now()
        return now.strftime("%c")

    def send_head(self):
        self.send_header("Server", self.server_name)
        self.send_header("Date", self.date_time_string())
        self.send_header("Content-Length", self.content_len)
        self.send_header("Content-Type", self.file_type)
        self.send_header("Connection", "Closed")
        self.end_headers()
        
    def send_file(self):
        f = open(self.path, 'rb')
        producer = FileProducer(f)
        file_data = bytes()
        while True:
            data = producer.more()
            if not data:
                break
            file_data += data
        self.send(file_data)   

    def do_GET(self):
        if self.path == '':
            self.path = 'index.html'
        try:
            f = open(self.path)
            f.close()
            self.file_type, _ = guess_type(self.path)
            self.content_len = os.path.getsize(self.path)
            self.send_response(code=200, message=responses[200][1])
            self.send_head()
            self.send_file()
        except FileNotFoundError:
            self.send_error(code=404, message=responses[404][1])
        except:
            self.send_error(code=403, message=responses[403][1])
        self.handle_close()
        

    def do_HEAD(self):
        if self.path == '':                
            self.path = 'index.html'
        try:
            self.file_type, _ = guess_type(self.path)
            self.content_len = os.path.getsize(self.path)
            self.send_response(code=200, message=responses[200][1])
            self.send_head()
        except PermissionError:
            self.send_error(code=403, message=responses[403][1])
        except FileNotFoundError:
            self.send_error(code=404, message=responses[404][1])
        self.handle_close()


def parse_args():
    parser = argparse.ArgumentParser("Simple asynchronous web-server")
    parser.add_argument("--host", dest="host", default="127.0.0.1")
    parser.add_argument("--port", dest="port", type=int, default=9000)
    parser.add_argument("--log", dest="loglevel", default="info")
    parser.add_argument("--logfile", dest="logfile", default=None)
    parser.add_argument("-w", dest="nworkers", type=int, default=1)
    parser.add_argument("-r", dest="document_root", default=".")
    return parser.parse_args()


def run(args):
    server = AsyncServer(host=args.host, port=args.port)
    server.serve_forever()


if __name__ == "__main__":
    args = parse_args()
    DOCUMENT_ROOT = args.document_root
    for _ in range(args.nworkers):
        p = multiprocessing.Process(target=run, args=(args,))
        p.start()
