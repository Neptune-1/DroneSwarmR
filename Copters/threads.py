import time
from threading import Thread

from Drone.FlightLib import FlightLib, LedLib
from Copters.StateMachine import StateMachine


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
            state_machine: StateMachine,
            frames: list
    ):
        super().__init__(name, socket)
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
    def __init__(self, name, socket, state_machine: StateMachine):
        super().__init__(name, socket)
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
