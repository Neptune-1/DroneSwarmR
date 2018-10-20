from Client import Client
from FlightLib import FlightLib
import time

# get self id
with open('id.txt') as file:
    copter_id = int(file.readline())


def programm():
    FlightLib.takeoff()
    time.sleep(10)
    FlightLib.land()


def programm_read():
    pass

if __name__ == "__main__":

    client = Client(copter_id)
    client.connect()

    start_wait_time = time.time()

    while True:
        data = client.recv()
        if (data == b'start'):
            programm()
            client.send('THE END!')
            break
        time.sleep(0.001)
        if (time.time() - start_wait_time > 10):
            break