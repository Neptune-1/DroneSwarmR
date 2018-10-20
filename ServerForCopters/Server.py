import socket
import logging
import sys


rootLogger = logging.getLogger()
rootLogger.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
rootLogger.addHandler(ch)


class Server(object):


    def __init__(self, HOST='localhost', PORT=8002):
        self.HOST = HOST
        self.PORT = PORT
        self.sock = socket.socket()
        self.sock.bind((self.HOST, self.PORT))
        self.sock.listen(2)
        self.copters = [None, None]


    def accept(self):
        while None in self.copters:
            conn, addr = self.sock.accept()
            info = conn.recv(1024).decode('utf-8')
            if(info == '1'):
                self.copters[0] = conn
                rootLogger.info("Connect copter 1 successfully!")
            elif(info == '2'):
                self.copters[1] = conn
                rootLogger.info("Connect copter 2 successfully!")

        rootLogger.info("Connect successfully!")


    def check(self):
        result = True
        # check copter 1
        self.copters[0].send(b'check')
        feedback = self.copters[0].recv(1024)
        if(feedback == b'OK!'):
            rootLogger.info('Copter 1 check successfully!')
        else:
            rootLogger.error('Error: Copter 1 check not successfully')
            result = False

        # check copter 2
        self.copters[1].send(b'check')
        feedback = self.copters[1].recv(1024)
        if (feedback == b'OK!'):
            rootLogger.info('Copter 2 check successfully!')
        else:
            rootLogger.error('Error: Copter 2 check not successfully')
            result = False

        return result


    def start(self):
        self.copters[0].send(b'start')
        self.copters[1].send(b'start')


    def wait_end(self):
        end = [False, False]
        while False in end:
            for i, el in enumerate(end):
                if el == False:
                    info = self.copters[i].recv(1024).decode('utf-8')
                    if info == 'THE END!': end[i] = True


    def close(self):
        self.copters[0].close()
        self.copters[1].close()
        self.sock.close()