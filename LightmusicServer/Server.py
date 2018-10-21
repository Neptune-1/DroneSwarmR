import socket
import logging
import sys


root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
ch.setFormatter(formatter)
root_logger.addHandler(ch)


class Server(object):
    def __init__(self, host='', port=9005):
        self.host = host
        self.port = port
        self.sock = socket.socket()
        self.sock.bind((host, port))
        self.sock.listen(2)
        self.copters = [None, None]
        self.accept()

    def accept(self):
        while None in self.copters:
            conn, addr = self.sock.accept()
            info = conn.recv(1024).decode('utf-8')
            if info == '1':
                self.copters[0] = conn
                root_logger.info("Connect copter 1 successfully!")
            elif info == '2':
                self.copters[1] = conn
                root_logger.info("Connect copter 2 successfully!")
        root_logger.info("Connect successfully!")

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

    def set_color(self, color=[0, 0, 0]):
        for copter in self.copters:
            color_str = ' '.join([str(s) for s in color])
            copter.send(('color ' + color_str).encode('utf-8'))

    def close(self):
        self.copters[0].send(b'close')
        self.copters[1].send(b'close')
        self.copters[0].close()
        self.copters[1].close()
        self.sock.close()
