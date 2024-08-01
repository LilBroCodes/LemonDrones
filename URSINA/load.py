import json
from typing import List, Dict
from collections import defaultdict


def load_and_process_stats(filename: str, target_fps: int = 60) -> List[Dict]:
    """
    Load state data from a JSON file, check for state changes, and limit the frame rate to a target FPS.

    Parameters:
    - filename (str): Path to the JSON file containing state data.
    - target_fps (int): Desired frames per second. Default is 60 FPS.

    Returns:
    - List[Dict]: Processed list of state records, limited to the target FPS.
    """

    with open(filename, "r") as file:
        data = json.load(file)

    grouped_by_second = defaultdict(list)

    for entry in data:
        timestamp = entry["timestamp"]
        second_part = int(timestamp)
        grouped_by_second[second_part].append(entry["state"])

    processed_states = []
    for states_in_second in grouped_by_second.values():
        if len(states_in_second) > target_fps:
            states_in_second = states_in_second[:target_fps]
        processed_states.extend(states_in_second)

    print(f"Processed {len(processed_states)} frames")

    return processed_states


def load_stats(filename: str, acc=False, need_y=False) -> list[dict]:
    """
    Load and process state statistics from a JSON file.

    This function reads a JSON file containing a list of state records, processes the data, and returns a list of
    dictionaries containing the selected state statistics. The selection of statistics to include in the output
    depends on the `acc` and `need_y` parameters.

    Parameters: - filename (str): The path to the JSON file containing the state records. The file is expected to be
    in JSON format with each record having a "state" key containing the relevant state data. - acc (bool): A flag
    indicating whether to include acceleration data in the output. If `True`, acceleration data will be included; if
    `False`, it will be excluded. Default is `False`. - need_y (bool): A flag indicating whether to include the
    `velocity_y` and `acceleration_y` fields in the output. If `False`, these fields will be excluded. Default is
    `False`.

    Returns: - list[dict]: A list of dictionaries where each dictionary represents a processed state record. The
    contents of each dictionary are determined by the `acc` and `need_y` parameters.
    """

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
            "timestamp": data[index].get("timestamp")
        } if acc else {
            "pitch": value["pitch"],
            "roll": value["roll"],
            "yaw": value["yaw"],
            "velocity_x": value["vgx"],
            "velocity_z": value["vgy"],
            "velocity_y": value["vgz"],
            "timestamp": data[index].get("timestamp")
        }
        if not need_y:
            need.pop("velocity_y")
            if acc:
                need.pop("acceleration_y")
        states[index] = need

    print(f"Loaded {len(states)} frames")
    return states
