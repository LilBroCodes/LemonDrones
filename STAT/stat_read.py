import time
from cv2 import imshow
import cv2
import djitellopy
from djitellopy.swarm import Tello
import sys


def ori(drone: djitellopy.Tello):
    state: dict
    state = drone.get_current_state()

    pitch, roll, yaw = state["pitch"], state["roll"], state["yaw"]
    vgx, vgy, vgz = state["vgx"], state["vgy"], state["vgz"]
    agx, agy, agz = state["agx"], state["agy"], state["agz"]
    return pitch, roll, yaw, vgx, vgy, vgz, agx, agy, agz

def msc(drone: djitellopy.Tello):
    state: dict
    state = drone.get_current_state()
    state.pop("vgx")


conn = Tello()
conn.connect()
conn.streamon()
try:
    while True:
        dat = ori(conn)
        for i in dat:
            print(dat)
        time.sleep(.2)
except KeyboardInterrupt:
    pass
finally:
    conn.end()
    sys.exit()
