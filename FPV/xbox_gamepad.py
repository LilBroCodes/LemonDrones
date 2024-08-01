from enum import Enum
from threading import Event, Thread
import evdev
from xbox_enums import *
import time

def pair_gp(return_type="path"):
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        if "xbox" in device.name.lower() and "controller" in device.name.lower():
            if return_type == "path":
                return device.path
            elif return_type == "id":
                return device.phys
            else:
                return device


class Gamepad:
    def __init__(self, pair=True, target=""):
        self.target: str
        self.ABS_ID: dict
        self.KEY_ID: dict
        self.gamepad: evdev.InputDevice
        self.running: bool
        self.key: list
        self.abs: list
        self._update_thread: Thread
        self._stop_event: Event
        self.running = False
        self._ABS_ID = {0: 0, 1: 1, 2: 2, 5: 3, 9: 4, 10: 5, 16: 6, 17: 7}
        self._KEY_ID = { 158: 0, 172: 1, 304: 2, 305: 3, 307: 4, 308: 5, 310: 6, 311: 7, 315: 8, 317: 9, 318: 10}
        if pair:
            self.target = pair_gp("path")
        else:
            self.target = target
        self.gamepad = evdev.InputDevice(self.target)
        self._stop_event = Event()
        self.key = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.abs = [32767, 32767, 32767, 32767, 0, 0, 0, 0]


    def _update(self):
        for event in self.gamepad.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                index = self._KEY_ID[event.code]
                self.key[index] = event.value
            elif event.type == evdev.ecodes.EV_ABS:
                index = self._ABS_ID[event.code]
                self.abs[index] = event.value



    def mainloop(self):
        if self.running: return
        self._update_thread = Thread(target=self._mainloop)
        self._update_thread.daemon = True
        self._update_thread.start()
        self.running = True

    def exit(self):
        self._stop_event.set()

    def _mainloop(self):
        while not self._stop_event.isSet():
            self._update()

class DroneGamepad:
    def __init__(self, deadzone=10):
        self.gamepad = Gamepad()
        self.deadzone_value = deadzone
        self.ud, self.lr, self.fb, self.yv = 0, 0, 0, 0
        self.tola = False
        self.do_pic = False
        self.do_vid = False

    def normalize_stick(self, x: int, y: int):
        nz_x = (x / 65535) * 2 - 1
        nz_y = (y / 65535) * 2 - 1

        scaled_x = nz_x * 50
        scaled_y = nz_y * 50

        if abs(scaled_x) < self.deadzone_value:
            scaled_x = 0
        if abs(scaled_y) < self.deadzone_value:
            scaled_y = 0

        return int(scaled_x), int(-scaled_y)

    def pressed(self, key: int) -> bool:
        return True if key == 1 else False

    def deadzone(self, dz: int, value) -> float:
        return 0 if dz > value else value

    def mainloop(self):
        self.gamepad.mainloop()
        while True:
            ls_x, ls_y = self.gamepad.abs[0], self.gamepad.abs[1]
            rs_x, rs_y = self.gamepad.abs[2], self.gamepad.abs[3]

            self.yv, self.fb = self.normalize_stick(ls_x, ls_y)
            self.lr, self.ud = self.normalize_stick(rs_x, rs_y)

            if self.pressed(self.gamepad.key[5]) and self.deadzone(5, self.gamepad.abs[4]) > 0:
                self.tola = True
            else:
                self.tola = False

            if self.deadzone(5, self.gamepad.abs[5]) > 0:
                self.do_pic = True
            else:
                self.do_pic = False

            if self.pressed(self.gamepad.key[6]):
                self.do_vid = True
            else:
                self.do_vid = False


    def start_thread(self):
        thread = Thread(target=self.mainloop)
        thread.start()
