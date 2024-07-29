import json


def load_stats(filename: str, acc=False, need_y=False) -> list[dict]:
    with open(filename, "r") as file:
        data = json.load(file)

    states = []
    for i in data:
        states.append(i.get("state"))

    for index, value in enumerate(states):
        need = {
            "pitch": value["pitch"],
            "roll": value["roll"],
            "yaw": value["yaw"],
            "velocity_x": value["vgx"],
            "velocity_z": value["vgy"],
            "velocity_y": value["vgz"],
            "acceleration_x": value["agx"],
            "acceleration_z": value["agy"],
            "acceleration_y": value["agz"],
        } if acc else {
            "pitch": value["pitch"],
            "roll": value["roll"],
            "yaw": value["yaw"],
            "velocity_x": value["vgx"],
            "velocity_z": value["vgy"],
            "velocity_y": value["vgz"]
        }
        if not need_y:
            need.pop("velocity_y")
            if acc:
                need.pop("acceleration_y")
        states[index] = need

    return states
