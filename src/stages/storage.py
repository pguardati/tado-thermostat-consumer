import json
import os


def read_json_files(source_dir):
    files = os.listdir(source_dir)
    data_list = []
    for file in files:
        with open(os.path.join(source_dir, file), "r") as f:
            raw_data = json.load(f)
        data_list.append(raw_data)
    return data_list
