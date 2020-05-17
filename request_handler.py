"""Webrequest routines"""
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
from socketserver import ThreadingMixIn
import time
from server_handler import ServerHandler


class Serv(BaseHTTPRequestHandler):
    """Class Serv"""

    def do_GET(self):
        """Handle Get Requests"""

        client = self.client_address[0]
        if not client in self.server.srvhandler.servers:
            response = "you fool"
            print("WARNING! Refused connection from " + client)
        else:
            self.server.srvhandler.set_server_time(client, time.time())
            queue = self.server.srvhandler.servers[client]
            if len(queue) > 0:
                data = queue[0]

                cmd = data[0]
                arg = data[1]

                print(str(client) + " << " + cmd + " " + arg)

                if cmd == "rcon":
                    arg = "game.ConsoleCommand[[" + arg + "\n]]"

                response = arg

                self.server.srvhandler.servers[client].pop(0)
            else:
                response = self.server.srvhandler.get_header()

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(bytes(response, 'utf-8'))

    def do_POST(self):
        """Handle POST Requests"""

        client = self.client_address[0]
        if not client in self.server.srvhandler.servers:
            print("WARNING! Refused POST connection from " + client)
        else:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            params = parse_qs(post_data.decode())
            try:
                if params['message'][0]:
                    print(str(client) + " >> " + params['message'][0])
                else:
                    print("Invalid postdata from " + str(client))
            except:
                print("Invalid postdata from " + str(client))
        self.send_response(200)
        self.end_headers()

    def log_message(self, format, *args):
        pass
    """Suspend connetion logs"""


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

    def __init__(self, server_address, handler, handler_class=Serv):
        super().__init__(server_address, handler_class)
        self.srvhandler = ServerHandler()
        self.srvhandler = handler
