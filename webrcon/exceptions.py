class InvalidServer(Exception):
    def __init__(self):
        super().__init__('Could not connect to server: server may not be running or invalid credentials used.')


class ConnectionClosed(Exception):
    def __init__(self):
        super().__init__('Connection to the WebSocket has been closed by the client.')