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

    Example: >>> load_stats('path/to/file.json', acc=True, need_y=False) [{'pitch': 0.1, 'roll': 0.2, 'yaw': 0.3,
    'velocity_x': 1.0, 'velocity_z': 1.1, 'acceleration_x': 0.5, 'acceleration_z': 0.6}, {'pitch': 0.2, 'roll': 0.3,
    'yaw': 0.4, 'velocity_x': 1.2, 'velocity_z': 1.3, 'acceleration_x': 0.7, 'acceleration_z': 0.8}]

    Notes: - The input JSON file is expected to be a list of dictionaries, where each dictionary has a "state" key
    with the state data. - The keys `"pitch"`, `"roll"`, `"yaw"`, `"vgx"`, `"vgy"`, `"vgz"`, `"agx"`, `"agy"`,
    and `"agz"` must be present in the state data. - If `acc` is `False`, acceleration-related fields (
    `"acceleration_x"`, `"acceleration_y"`, `"acceleration_z"`) will be omitted from the output. - If `need_y` is
    `False`, the `"velocity_y"` and `"acceleration_y"` fields will be omitted from the output if `acc` is `True`.

    Example JSON data: [ {"state": {"pitch": 0.1, "roll": 0.2, "yaw": 0.3, "vgx": 1.0, "vgy": 1.1, "vgz": 1.2,
    "agx": 0.5, "agy": 0.6, "agz": 0.7}}, {"state": {"pitch": 0.2, "roll": 0.3, "yaw": 0.4, "vgx": 1.2, "vgy": 1.3,
    "vgz": 1.4, "agx": 0.7, "agy": 0.8, "agz": 0.9}} ]
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
