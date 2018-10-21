from logger import root_logger

import socket


class Server(object):
    def __init__(self, host='', port=8002):
        self.host = host
        self.port = port
        self.sock = socket.socket()
        self.sock.bind((self.host, self.port))
        self.sock.listen(2)
        self.copters = [None, None]

    def run(self):
        self.accept()
        self.takeoff()

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

    def check(self):
        result = True
        # check copter 1
        self.copters[0].send(b'check')
        feedback = self.copters[0].recv(1024)
        if feedback == b'OK!':
            root_logger.info('Copter 1 check successfully!')
        else:
            root_logger.error('Error: Copter 1 check not successfully')
            result = False

        # check copter 2
        self.copters[1].send(b'check')
        feedback = self.copters[1].recv(1024)
        if feedback == b'OK!':
            root_logger.info('Copter 2 check successfully!')
        else:
            root_logger.error('Error: Copter 2 check not successfully')
            result = False
        return result

    def takeoff(self):
        for copter in self.copters:
            copter.send(b'takeoff')

    def land(self):
        for copter in self.copters:
            copter.send(b'land')

    def pause(self):
        for copter in self.copters:
            copter.send(b'pause')

    def resume(self):
        for copter in self.copters:
            copter.send(b'resume')

    def start_animation(self):
        for copter in self.copters:
            copter.send(b'start_animation')

    def close(self):
        self.copters[0].close()
        self.copters[1].close()
        self.sock.close()
