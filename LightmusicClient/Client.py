import socket


class Client(object):
    def __init__(self, host='localhost', port=9000):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
        self.host = host

    def connect(self):
        self.sock.connect((self.host, self.port))
        self.sock.send(b'1')

    def get_data(self):
        data = self.sock.recv(1024)
        data = data.decode('utf-8')
        return data