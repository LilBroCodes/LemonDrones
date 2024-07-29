import json

input_file = "state_log_d2.json"

with open(input_file, "r") as file:
    data = json.loads(file.read())

base_time = 0
for i, value in enumerate(data):
    if i == 0:
        base_time = value["timestamp"]
        print(base_time)

    value["timestamp"] = value["timestamp"] - base_time
    print(value["timestamp"])

with open(f"{input_file.split('.')[0]}-relative.json", "w") as file:
    json.dump(data, file, indent=1)
