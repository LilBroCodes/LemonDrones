from enum import Enum

class ABS(Enum):
    LEFT_STICK_X = 0
    LEFT_STICK_Y = 1

    RIGHT_STICK_X = 2
    RIGHT_STICK_Y = 3

    TRIGGER_RIGHT = 4
    TRIGGER_LEFT = 5

    DPAD_X = 6
    DPAD_Y = 7

class KEY(Enum):
    BTN_SELECT = 0
    BTN_LOGO = 1
    BTN_A = 2
    BTN_B = 3
    BTN_X = 4
    BTN_Y = 5
    LEFT_SHOULDER = 6
    RIGHT_SHOULDER = 7
    BTN_START = 8
    LEFT_STICK_DOWN = 9
    RIGHT_STICK_DOWN = 10
