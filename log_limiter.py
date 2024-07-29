import json


def load_and_limit_fps(filename: str, target_fps: int) -> list[dict]:
    """
    Load data from a JSON file and limit the frames to the specified FPS.

    This function reads a JSON file containing state records with timestamps and reduces the frame rate to the specified target FPS.

    Parameters:
    - filename (str): The path to the JSON file containing the state records.
    - target_fps (int): The target frame rate (frames per second) to limit the data to.

    Returns:
    - list[dict]: A list of dictionaries containing the reduced frame data.

    Example:
    >>> load_and_limit_fps('path/to/file.json', target_fps=60)
    [{'timestamp': 0.0, 'state': {...}}, {'timestamp': 0.0167, 'state': {...}}, ...]
    """

    # Load data from the JSON file
    with open(filename, "r") as file:
        data = json.load(file)

    # Initialize variables
    frame_interval = 1 / target_fps
    reduced_data = []
    last_timestamp = None

    # Process each record
    for record in data:
        timestamp = record["timestamp"]

        if last_timestamp is None or (timestamp - last_timestamp) >= frame_interval:
            reduced_data.append(record)
            last_timestamp = timestamp

    print(f"Original frames: {len(data)}, Reduced frames: {len(reduced_data)}")
    return reduced_data


# Example usage
if __name__ == "__main__":
    filename = 'state_log_4_fastloop.json'
    target_fps = 60
    reduced_data = load_and_limit_fps(filename, target_fps)
    with open('state_log_4_fastloop-60FPS.json', 'w') as outfile:
        json.dump(reduced_data, outfile, indent=4)
