"""Input Handling Routines"""
import time
import os
from server_handler import ServerHandler
from server_cmd import ServerCommandHandler


class InputHandler():
    """Class InputHandler"""

    def __init__(self, serverhandler, servercmdhandler):
        """Constructor"""
        self.srvhandler = ServerHandler()
        self.srvhandler = serverhandler

        self.cmdhandler = ServerCommandHandler(serverhandler)
        self.cmdhandler = servercmdhandler

    def handle_console_input(self, originalInput):
        """Main Input func. Todo: split"""
        cmd = originalInput.split(" ")

        if originalInput == "list":
            for k in self.srvhandler.servers.keys():
                online = self.srvhandler.server_time[k]['curtime'] + \
                    10 >= time.time()
                print(k + " | Online: " + str(online))
            return

        try:
            command = cmd[0]
            arg = cmd[1]

        except Exception:
            print("[1] No such command: " + originalInput)
            return

        if command == "addserver":
            with open('server.list', 'a') as file:
                if os.stat("server.list").st_size == 0:
                    file.write(arg)
                else:
                    file.write('\n' + arg)
            self.srvhandler.servers[arg] = []
            self.srvhandler.set_server_time(arg, 0)
            print('Successful added ' + arg + ' to the list')
            return
        if command == "selectserver":
            if arg not in self.srvhandler.servers:
                print("No such server found.")
                return
            self.srvhandler.set_current_server(arg)
            print("Successfully selected server: " +
                  self.srvhandler.get_current_server())
            return

        try:

            if self.cmdhandler.commands[command]:
                if self.srvhandler.get_current_server() == "nil":
                    print(
                        "No server selected. ",
                        "Select a server by using selectserver [ip]")
                    return
                self.cmdhandler.commands[command](command, originalInput)
                return
        except Exception:
            print("[2] Wrong syntax: " + command)

    def read_input(self):
        while True:
            original_input = input()
            self.handle_console_input(original_input)
