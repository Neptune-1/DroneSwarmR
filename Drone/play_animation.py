import time
import csv

from FlightLib import FlightLib
FlightLib.init('SingleCleverFlight')
from FlightLib import LedLib


animation_file_path = 'animation.csv'
frames = []


def takeoff():
    FlightLib.takeoff()
    LedLib.wipe_to(0, 255, 0)


def land():
    LedLib.rainbow()
    FlightLib.land()
    LedLib.off()


def do_next_animation(current_frame):
    FlightLib.navto(
        round(float(current_frame['x']), 4), round(float(current_frame['y']), 4), round(float(current_frame['z']), 4),
        round(float(current_frame['yaw']), 4), speed=2
    )
    LedLib.fill(
        int(current_frame['green']), int(current_frame['red']), int(current_frame['blue'])
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
        do_next_animation(frame)
        time.sleep(0.1)
    land()
    time.sleep(3)
