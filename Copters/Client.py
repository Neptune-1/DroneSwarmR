import socket
import csv

from config import Config
from Copters.StateMachine import StateMachine
from Copters.threads import ServerPollingThread, FlyingThread


class Client(object):
    def __init__(self, host='localhost', port=8002):
        self.state_machine = StateMachine(
            start_state=StateMachine.PAUSE_STATE
        )
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
        self.host = host
        self.copter_id = Config.copter_id
        self.frames = []
        self.animation_file_path = Config.animation_file_path
        self.read_animation_file()

    def read_animation_file(self):
        with open(self.animation_file_path) as animation_file:
            csv_reader = csv.reader(
                animation_file, delimiter=',', quotechar='|'
            )
            for row in csv_reader:
                frame_number, x, y, z, speed, red, green, blue = row
                self.frames.append({
                    'number': frame_number,
                    'x': x,
                    'y': y,
                    'z': z,
                    'speed': speed,
                    'red': red,
                    'green': green,
                    'blue': blue
                })

    def run(self):
        self.socket.connect((self.host, self.port))
        self.socket.listen(2)
        self.socket.send(str(self.copter_id).encode('utf-8'))
        server_polling_thread = ServerPollingThread(
            'server_polling', self.socket, self.state_machine
        )
        animation_thread = FlyingThread(
            'animation', self.socket, self.state_machine, self.frames
        )
        server_polling_thread.start()
        animation_thread.start()
