import json
import time

from djitellopy import tello

conn = tello.Tello()
conn.connect()


def get_drone_state():
    while True:
        state = conn.get_current_state()
        timestamp = time.time()
        states.append({'timestamp': timestamp, 'state': state})
        print({'timestamp': timestamp, 'state': state})


states = []

try:
    while True:
        get_drone_state()
except KeyboardInterrupt:
    pass
finally:
    with open('state_log_3_inhand.json', 'w') as file:
        json.dump(states, file, indent=4)
    conn.end()
    exit(0)
