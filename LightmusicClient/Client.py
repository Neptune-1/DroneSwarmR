import socket
import time

from FlightLib import LedLib


class Config:
    copter_id = 1  # os.environ.get('COPTER_ID')
    host = "192.168.43.19"  # os.environ.get('HOST')
    animation_file_path = 'drone{}.csv'.format(copter_id)


class Client(object):
    def __init__(self, host=Config.host, port=9000):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
        self.host = host

    def run(self):
        self.connect()
        red = 0
        green = 0
        blue = 0
        while True:
            data = self.fetch_data()
            if 'color' in data:
                data = data.split()[1:]
                color = map(int, data)
                red, green, blue = color
            elif data == 'rainbow':
                LedLib.rainbow()
            elif data == 'fill':
                LedLib.fill(red, green, blue)
            elif data == 'blink':
                LedLib.blink(red, green, blue)
            elif data == 'chase':
                LedLib.chase(red, green, blue)
            elif data == 'wipe_to':
                LedLib.wipe_to(red, green, blue)
            elif data == 'fade_to':
                LedLib.fade_to(red, green, blue)
            elif data == 'run':
                LedLib.fade_to(red, green, blue)
            elif data == 'close':
                LedLib.off()
            time.sleep(0.001)

    def connect(self):
        self.sock.connect((self.host, self.port))
        self.sock.send(str(Config.copter_id))

    def close(self):
        self.sock.close()

    def fetch_data(self):
        data = self.sock.recv(1024)
        data = data.decode('utf-8')
        return data
