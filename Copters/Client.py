import socket


class Client(object):
    def __init__(self, copter_id, HOST='localhost', PORT=8002):
        self.PORT = PORT
        self.HOST = HOST
        self.copter_id = copter_id
        self.sock = socket.socket()


    def connect(self):
        self.sock.connect((self.HOST, self.PORT))
        self.sock.send(str(self.copter_id).encode('utf-8'))


    def recv(self):
        data = self.sock.recv(1024).decode('utf-8')
        return data


    def send(self, data):
        self.sock.send(data.encode('utf-8'))
