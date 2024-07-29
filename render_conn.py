from ursina import *
from ursina.shaders import *
import djitellopy as tello

SPEED = 10
R_SPEED = 10

app = Ursina()

model_path = "dji_tello.glb"
model_drone = Entity(model=model_path, scale=2, collider='box', position=(0, 1, 0), shader=basic_lighting_shader)

Sky(texture=load_texture("sky_sunset"))

ground = Entity(
    model='plane',
    texture='grass',
    collider='mesh',
    scale=(1000, 1, 1000),
    position=(0, 0, 0),
    shader=lit_with_shadows_shader
)

rotation_multiplier = 1

drone = tello.Tello()


def connect_drone():
    drone.connect()
    drone.streamon()


connect_drone()


def normalize_angle(angle):
    while angle > 180:
        angle -= 360
    while angle < -180:
        angle += 360
    return angle


def shortest_angle(current_angle, target_angle):
    delta_angle = target_angle - current_angle
    if delta_angle > 180:
        delta_angle -= 360
    elif delta_angle < -180:
        delta_angle += 360
    return delta_angle


def update():
    global drone

    if held_keys['w']:
        drone.move_forward(SPEED)
    if held_keys['s']:
        drone.move_back(SPEED)
    if held_keys['a']:
        drone.move_left(SPEED)
    if held_keys['d']:
        drone.move_right(SPEED)
    if held_keys['up arrow']:
        drone.move_up(SPEED)
    if held_keys['down arrow']:
        drone.move_down(SPEED)
    if held_keys['q']:
        drone.rotate_counter_clockwise(R_SPEED)
    if held_keys['e']:
        drone.rotate_clockwise(R_SPEED)
    if held_keys['r']:
        drone.move_up(SPEED)
    if held_keys['f']:
        drone.move_down(SPEED)
    if held_keys['o']:
        drone.takeoff()
    if held_keys['l']:
        drone.land()

    state = drone.get_current_state()

    pitch = state.get('pitch', 0)
    roll = state.get('roll', 0)
    yaw = state.get('yaw', 0)
    vgx = state.get('vgx', 0) / 10
    vgy = state.get('vgy', 0) / 10
    vgz = state.get('vgz', 0) / 10

    current_yaw = model_drone.rotation_y
    target_yaw = normalize_angle(yaw * rotation_multiplier)
    delta_yaw = shortest_angle(current_yaw, target_yaw)

    current_pitch = model_drone.rotation_x
    target_pitch = normalize_angle(pitch * rotation_multiplier)
    delta_pitch = shortest_angle(current_pitch, target_pitch)

    current_roll = model_drone.rotation_z
    target_roll = normalize_angle(roll * rotation_multiplier)
    delta_roll = shortest_angle(current_roll, target_roll)

    new_rotation = Vec3(
        int(current_pitch + delta_pitch),
        int(current_yaw + delta_yaw),
        int(current_roll + delta_roll)
    )
    model_drone.rotation = new_rotation

    new_position = model_drone.position + Vec3(vgz, vgy, -vgx)
    model_drone.position = new_position


EditorCamera()
app.run()
