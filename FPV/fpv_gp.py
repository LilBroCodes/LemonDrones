from threading import Event, Thread
from cv2.gapi import BGR2RGB
from djitellopy import Tello
import djitellopy
import cv2
import numpy as np
import os
import time
import pygame
from xbox_gamepad import DroneGamepad
from datetime import datetime as dt

pygame.init()

stream_ready = Event()

SCREEN_WIDTH, SCREEN_HEIGHT = 960, 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tello FPV")

lr = 0
fb = 0
ud = 0
yv = 0

drone = Tello()
drone.connect()
battery_level = drone.get_battery()
print(f"Battery level: {battery_level}%")
drone.streamon()
frame_read = drone.get_frame_read()

gamepad = DroneGamepad(5)
gamepad.start_thread()

last_special = 0
in_air = False

def tola():
    global in_air
    if in_air:
        in_air = False
        drone.land()
    elif not in_air:
        in_air = True
        drone.takeoff()
    pass

def handle_input(drone: djitellopy.Tello):
    global ud, fb, lr, yv

    fb, yv = gamepad.fb, gamepad.yv
    ud = gamepad.ud
    lr = gamepad.lr * 2
    # ud = 0

    if last_special == 0 or time.time() - last_special > 2:
        if gamepad.tola:
            tola()



def take_picture(frame) -> None:
    try:
        if not os.path.exists("pictures"):
            os.mkdir("pictures")
        file_name = f"pictures/{dt.now().strftime('%m-%d %H-%M-%S')}.png"
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.imwrite(file_name, frame)
        print(f"Image saved: {file_name}")
        last_special = time.time()
    except Exception as e:
        print("Error thrown in take_picture: ", str(e))


def display_frame():
    frame = frame_read.frame
    if last_special == 0 or time.time() - last_special > 2:
        if gamepad.do_pic:
            take_picture(frame)
    frame = np.rot90(frame)
    frame = np.flipud(frame)
    frame = pygame.surfarray.make_surface(frame)
    screen.blit(frame, (0, 0))

def control():
    global lr, fb, ud, yv
    while True:
        handle_input(drone)
        drone.send_rc_control(lr, fb, ud, yv)

def main():
    print(f"Battery: {drone.get_battery()}%")
    try:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            display_frame()
            pygame.time.delay(50)
            pygame.display.flip()
            if not stream_ready.is_set():
                stream_ready.set()

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if in_air:
            drone.land()
        drone.streamoff()
        pygame.quit()

if __name__ == "__main__":
    render_thread = Thread(target=main)
    render_thread.daemon = True
    render_thread.start()
    control()
