"""Main Module"""
import threading
from server_handler import ServerHandler
from server_cmd import ServerCommandHandler
from request_handler import ThreadedHTTPServer, Serv
from input_handler import InputHandler

PORT = 27015


def main():
    """Main Function"""
    servhandler = ServerHandler()
    servcmd = ServerCommandHandler(servhandler)
    inputhandler = InputHandler(servhandler, servcmd)

    if servhandler.get_header() == "nil":
        return
    servhandler.load_servers()
    httpd = ThreadedHTTPServer(('', PORT), servhandler, Serv)
    print("AppleCon 0.2 loaded (Made by AppleJeb, mod by zuknes)")
    print("Listening on port " + str(PORT))
    print("Type addserver [ip] to vzlomhack()")

    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.start()

    while True:
        inputhandler.read_input()


if __name__ == "__main__":
    main()
