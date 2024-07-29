import threading
from djitellopy import Tello
import time
import json

tello = Tello()
tello.connect()

states = []

print(tello.get_battery())


def get_drone_state():
    while True:
        state = tello.get_current_state()
        timestamp = time.time()
        states.append({'timestamp': timestamp, 'state': state})
        time.sleep(0.5)


def main():
    tello.takeoff()
    time.sleep(5)  # Ensure the drone is stable after takeoff
    tello.rotate_clockwise(360)
    time.sleep(8)  # Wait for the rotation to complete (adjust timing if needed)
    tello.move_forward(75)
    time.sleep(5)  # Wait for the forward movement to complete (adjust timing if needed)
    tello.rotate_clockwise(360)
    time.sleep(8)  # Wait for the rotation to complete (adjust timing if needed)
    tello.land()


try:
    state_thread = threading.Thread(target=get_drone_state)
    main_thread = threading.Thread(target=main)

    state_thread.start()
    main_thread.start()

    main_thread.join()
    state_thread.join()
except KeyboardInterrupt:
    tello.land()
finally:
    with open('state_log_4_fastloop.json', 'w') as file:
        json.dump(states, file, indent=4)
    tello.end()
    exit(0)
