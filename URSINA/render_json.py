from ursina import *
from ursina.shaders import *
from load import load_stats
import time

anim = load_stats("state_log_4_fastloop-relative.json", need_y=True)
app = Ursina()

model_path = "dji_tello.glb"
drone = Entity(model=model_path, scale=2, collider='box', position=(0, 1, 0), shader=basic_lighting_shader)

Sky(texture=load_texture("sky_sunset"))

ground = Entity(
    model='plane',
    texture='grass',
    collider='mesh',
    scale=(1000, 1, 1000),
    position=(0, 0, 0),
    shader=lit_with_shadows_shader
)

frame_id = 0
last_update_time = time.time()
rotation_multiplier = 1


def normalize_angle(angle):
    """Normalize an angle to the range [-180, 180]."""
    while angle > 180:
        angle -= 360
    while angle < -180:
        angle += 360
    return angle


def shortest_angle(current_angle, target_angle):
    """Calculate the shortest angle between two angles."""
    delta_angle = target_angle - current_angle
    if delta_angle > 180:
        delta_angle -= 360
    elif delta_angle < -180:
        delta_angle += 360
    return delta_angle


def update():
    global frame_id, last_update_time

    current_time = time.time()
    elapsed_time = current_time - last_update_time
    frame_timestamp = anim[frame_id]["timestamp"]

    if elapsed_time >= frame_timestamp:
        frame = anim[frame_id]
        if frame_id + 1 < len(anim):
            next_timestamp = anim[frame_id + 1]["timestamp"]
            delay = next_timestamp - frame_timestamp

            current_yaw = drone.rotation_y
            target_yaw = normalize_angle(frame["yaw"] * rotation_multiplier)
            delta_yaw = shortest_angle(current_yaw, target_yaw)

            current_pitch = drone.rotation_x
            target_pitch = normalize_angle(frame["pitch"] * rotation_multiplier)
            delta_pitch = shortest_angle(current_pitch, target_pitch)

            current_roll = drone.rotation_z
            target_roll = normalize_angle(frame["roll"] * rotation_multiplier)
            delta_roll = shortest_angle(current_roll, target_roll)

            new_rotation = Vec3(
                int(current_pitch + delta_pitch),
                int(current_yaw + delta_yaw),
                int(current_roll + delta_roll)
            )
            drone.animate_rotation(new_rotation, duration=delay, curve=curve.linear)

            new_position = drone.get_position() + Vec3(frame["velocity_z"], frame["velocity_y"], -frame["velocity_x"])
            drone.animate_position(new_position, delay, curve=curve.linear)

        frame_id += 1
        if frame_id == len(anim):
            frame_id = 0


EditorCamera()
app.run()
