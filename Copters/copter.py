from Client import Client
from FlightLib import FlightLib
import time

copter_id = 1


def programm():
    FlightLib.takeoff()
    time.sleep(10)
    FlightLib.land()


if __name__ == "__main__":

    client = Client(copter_id)
    client.connect()

    start_wait_time = time.time()

    while True:
        data = client.recv()
        if(data == b'start'):
            programm()
            client.
            break
        time.sleep(0.001)
        if(time.time() - start_wait_time > 10):
            break