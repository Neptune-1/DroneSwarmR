import time
import csv

from FlightLib import FlightLib
FlightLib.init('SingleCleverFlight')
from FlightLib import LedLib


animation_file_path = 'drone1.csv'
frames = []
current_frame_number = 1


def takeoff():
    FlightLib.takeoff()
    LedLib.rainbow()


def land():
    FlightLib.land()
    LedLib.off()


def do_next_animation():
    current_frame = frames[current_frame_number]
    FlightLib.navto(
        current_frame['x'], current_frame['y'], current_frame['z'],
        current_frame['yaw'], speed=current_frame['speed']
    )
    LedLib.fade_to(
        current_frame['r'], current_frame['g'], current_frame['b']
    )


def read_animation_file():
    with open(animation_file_path) as animation_file:
        csv_reader = csv.reader(
            animation_file, delimiter=',', quotechar='|'
        )
        for row in csv_reader:
            frame_number, x, y, z, speed, red, green, blue, yaw = row
            frames.append({
                'number': frame_number,
                'x': x,
                'y': y,
                'z': z,
                'speed': speed,
                'red': red,
                'green': green,
                'blue': blue,
                'yaw': yaw
            })


if __name__ == '__main__':
    read_animation_file()
    takeoff()
    for frame in frames:
        do_next_animation()
        time.sleep(0.1)
        current_frame_number += 1
    land()
