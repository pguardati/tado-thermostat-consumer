import json
import os

import pandas as pd


def write_to_parquet(dataframe, destination_dir, file_name):
    dataframe.to_parquet(os.path.join(destination_dir, f"{file_name}.parquet"))


def read_parquet_file(source_dir, file_name):
    return pd.read_parquet(os.path.join(source_dir, f"{file_name}.parquet"))


def read_json_files(source_dir):
    files = os.listdir(source_dir)
    data_list = []
    for file in files:
        with open(os.path.join(source_dir, file), "r") as f:
            raw_data = json.load(f)
        data_list.append(raw_data)
    return data_list


def read_jsonlist_write_parquet(func):
    def wrapper(source_dir, destination_dir, file_name_destination):
        raw_data_list = read_json_files(source_dir)

        processed_data = [func(data) for data in raw_data_list]
        _processed = pd.concat(processed_data)

        write_to_parquet(_processed, destination_dir, file_name_destination)
        return _processed

    return wrapper


def read_parquet_write_parquet(func):
    def wrapper(
        source_dir, destination_dir, file_name_source, file_name_destination, settings
    ):
        df = read_parquet_file(source_dir, file_name_source)
        processed_df = func(df, settings)
        write_to_parquet(processed_df, destination_dir, file_name_destination)
        return processed_df

    return wrapper
