from __future__ import print_function
import time

from Drone.FlightLib import LedLib
from Client import Client


if __name__ == '__main__':
    client = Client()
    client.connect()

    print("Connect success")

    red = 0
    green = 0
    blue = 0

    while True:
        data = client.get_data()
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