import socket
import logging
import sys


rootLogger = logging.getLogger()
rootLogger.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
ch.setFormatter(formatter)
rootLogger.addHandler(ch)


class Server(object):
    def __init__(self, host='localhost', port=9000):
        self.host = host
        self.port = port
        self.sock = socket.socket()
        self.sock.bind((host, port))
        self.sock.listen(2)
        self.copters = [None, None]

    def accept(self):
        while None in self.copters:
            conn, addr = self.sock.accept()
            info = conn.recv(1024).decode('utf-8')
            if info == '1':
                self.copters[0] = conn
                rootLogger.info("Connect copter 1 successfully!")
            elif info == '2':
                self.copters[1] = conn
                rootLogger.info("Connect copter 2 successfully!")
        rootLogger.info("Connect successfully!")

    def rainbow(self):
        for copter in self.copters:
            copter.send(b'rainbow')

    def fill(self):
        for copter in self.copters:
            copter.send(b'fill')

    def blink(self):
        for copter in self.copters:
            copter.send(b'blink')

    def chase(self):
        for copter in self.copters:
            copter.send(b'chase')

    def wipe_to(self):
        for copter in self.copters:
            copter.send(b'wipe_to')

    def fade_to(self):
        for copter in self.copters:
            copter.send(b'fade_to')

    def run(self):
        for copter in self.copters:
            copter.send(b'run')

    def set_color(self, color=(0, 0, 0)):
        for copter in self.copters:
            color = ' '.join(list(map(str, color)))
            copter.send('color ' + color)

    def close(self):
        self.copters[0].send(b'close')
        self.copters[1].send(b'close')
        self.copters[0].close()
        self.copters[1].close()
        self.sock.close()