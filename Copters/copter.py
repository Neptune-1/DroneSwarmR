import socket
import csv
import time
from threading import Thread

from FlightLib import FlightLib
FlightLib.init('SingleCleverFlight')
from FlightLib import LedLib


class Config:
    copter_id = 1  # os.environ.get('COPTER_ID')
    host = "192.168.43.19"  # os.environ.get('HOST')
    animation_file_path = 'drone{}.csv'.format(copter_id)


class StateMachine(object):
    TAKING_OFF_STATE = 0
    ANIMATION_STATE = 1
    PAUSE_STATE = 2
    LANDING_STATE = 3

    def __init__(self, start_state=PAUSE_STATE):
        self.state = start_state

    def switch_state(self, new_state):
        self.state = new_state


class Threadable(Thread):
    def __init__(self, name, socket):
        Thread.__init__(self)
        self.name = name
        self.socket = socket

    def fetch_from_server(self):
        data = self.socket.recv(1024).decode('utf-8')
        return data

    def send_to_server(self, data):
        self.socket.send(data.encode('utf-8'))


class FlyingThread(Threadable):
    def __init__(
            self,
            name,
            socket,
            state_machine,
            frames
    ):
        super(FlyingThread, self).__init__(name, socket)
        self.current_frame_number = 0
        self.state_machine = state_machine
        self.frames = frames

    def run(self):
        delay = 0.01
        while True:
            if self.state_machine.state == StateMachine.ANIMATION_STATE:
                self.do_next_animation()
            elif self.state_machine.state == StateMachine.TAKING_OFF_STATE:
                self.takeoff()
            elif self.state_machine.state == StateMachine.LANDING_STATE:
                self.land()
            else:
                time.sleep(delay)

    def takeoff(self):
        FlightLib.takeoff()
        LedLib.rainbow()
        self.state_machine.switch_state(
            new_state=StateMachine.PAUSE_STATE
        )

    def land(self):
        FlightLib.land()
        LedLib.off()
        self.state_machine.switch_state(
            new_state=StateMachine.PAUSE_STATE
        )

    def do_next_animation(self):
        current_frame = self.frames[self.current_frame_number]
        FlightLib.reach(
            current_frame['x'], current_frame['y'], current_frame['z'],
            speed=current_frame['speed']
        )
        LedLib.fade_to(
            current_frame['r'], current_frame['g'], current_frame['b']
        )


class ServerPollingThread(Threadable):
    def __init__(self, name, socket, state_machine):
        super(ServerPollingThread, self).__init__(name, socket)
        self.paused = False
        self.state_machine = state_machine

    def run(self):
        while True:
            data = self.fetch_from_server()
            if data == b'takeoff':
                self.takeoff()
            elif data == b'start_animation':
                self.start_animation()
            elif data == b'pause':
                self.pause()
            elif data == b'resume':
                self.resume()
            elif data == b'land':
                self.land()
            time.sleep(0.005)

    def takeoff(self):
        self.state_machine.switch_state(
            new_state=StateMachine.TAKING_OFF_STATE
        )

    def start_animation(self):
        self.state_machine.switch_state(
            new_state=StateMachine.ANIMATION_STATE
        )

    def pause(self):
        self.state_machine.switch_state(
            new_state=StateMachine.PAUSE_STATE
        )

    def resume(self):
        self.state_machine.switch_state(
            new_state=StateMachine.ANIMATION_STATE
        )

    def land(self):
        self.state_machine.switch_state(
            new_state=StateMachine.LANDING_STATE
        )


class Client(object):
    def __init__(self, host=Config.host, port=8002):
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



    def run(self):
        connected = False
        while not connected:
            try:
                self.socket.bind((self.host, self.port))
                if self.socket.
                connection_set = True
            except Exception as e:
                pass
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


if __name__ == "__main__":
    client = Client()
    client.run()
