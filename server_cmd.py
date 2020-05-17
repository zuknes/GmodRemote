"""Server command routines"""
from server_handler import ServerHandler


class ServerCommandHandler():
    """ServerCommandHandler"""

    def __init__(self, serverhandler):
        """Constructor"""
        self.srvhandler = ServerHandler()
        self.srvhandler = serverhandler

        self.commands = {
            'luarun': self.command_luarun,
            'rcon': self.command_rcon,
            'sendfile': self.command_sendfile,
        }

    def queue_command(self, serverip, arg_type, arg_command):
        """Queue Server Command"""
        self.srvhandler.servers[serverip].append([arg_type, arg_command])

    def command_luarun(self, arg_command, arg_input):
        """Luarun"""
        tosend = arg_input[len(arg_command) + 1:]
        self.queue_command(self.srvhandler.get_current_server(),
                           arg_command, tosend)
        print("luarun " + tosend + ">>" + self.srvhandler.get_current_server())

    def command_rcon(self, arg_command, arg_input):
        """Rcon"""
        tosend = arg_input[len(arg_command) + 1:]
        self.queue_command(self.srvhandler.get_current_server(),
                           arg_command, tosend)
        print("rcon " + tosend + ">>" + self.srvhandler.get_current_server())

    def command_sendfile(self, arg_command, arg_input):
        """SendFile"""
        tosend = arg_input[len(arg_command) + 1:]
        try:
            file_container = open('./includes/' + tosend + '.lua', 'r').read()
        except:
            print("Error opening file: " + tosend + '.lua')
            return
        self.queue_command(self.srvhandler.get_current_server(),
                           'luarun', file_container)
        print("luarun " + tosend + ">>" + self.srvhandler.get_current_server())
