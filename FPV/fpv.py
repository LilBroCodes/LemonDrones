from cv2.gapi import BGR2RGB
from djitellopy import Tello
import djitellopy
import pygame
import cv2
import numpy as np
import os
import time

# Initialize Pygame
pygame.init()

# Define screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 960, 720

# Set up the Pygame screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tello FPV")

# Define control variables
left_right_velocity = 0
forward_backward_velocity = 0
up_down_velocity = 0
yaw_velocity = 0

# Initialize the Tello drone
tello = Tello()
tello.connect()
battery_level = tello.get_battery()
print(f"Battery level: {battery_level}%")
tello.streamon()
frame_read = tello.get_frame_read()

def handle_input(drone: djitellopy.Tello):
    global left_right_velocity, forward_backward_velocity, up_down_velocity, yaw_velocity
    keys = pygame.key.get_pressed()

    speed = 50
    r_speed = 250
    # Control velocities based on key presses
    if keys[pygame.K_w]:
        forward_backward_velocity = speed
    elif keys[pygame.K_s]:
        forward_backward_velocity = -speed
    else:
        forward_backward_velocity = 0

    if keys[pygame.K_a]:
        left_right_velocity = -speed
    elif keys[pygame.K_d]:
        left_right_velocity  = speed
    else:
        left_right_velocity = 0

    if keys[pygame.K_UP]:
        up_down_velocity = speed
    elif keys[pygame.K_DOWN]:
        up_down_velocity = -speed
    else:
        up_down_velocity = 0

    if keys[pygame.K_LEFT]:
        yaw_velocity = -r_speed
    elif keys[pygame.K_RIGHT]:
        yaw_velocity = r_speed
    else:
        yaw_velocity = 0

    if keys[pygame.K_o]:
        tello.takeoff()

    if keys[pygame.K_l]:
        tello.land()


def take_picture(frame) -> None:
    try:
        if not os.path.exists("pictures"):
            os.mkdir("pictures")
        file_name = f"pictures/{time.time()}.png"
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.imwrite(file_name, frame)
        print(f"Image saved: {file_name}")
        time.sleep(.3)
    except Exception as e:
        print("Error thrown in take_picture: ", str(e))


def display_frame():
    frame = frame_read.frame
    keys = pygame.key.get_pressed()
    if keys[pygame.K_p]:
        take_picture(frame)
    frame = np.rot90(frame)
    frame = np.flipud(frame)
    frame = pygame.surfarray.make_surface(frame)
    screen.blit(frame, (0, 0))
    pygame.display.update()

def main():
    global left_right_velocity, forward_backward_velocity, up_down_velocity, yaw_velocity

    try:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            handle_input(tello)
            tello.send_rc_control(left_right_velocity, forward_backward_velocity, up_down_velocity, yaw_velocity)
            display_frame()
            pygame.time.delay(50)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        tello.land()
        tello.streamoff()
        pygame.quit()

if __name__ == "__main__":
    main()
