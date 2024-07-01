import pandas as pd

from src.common import read_jsonlist_write_parquet


@read_jsonlist_write_parquet
def get_daily_temperature(raw_row):
    temperatures = raw_row["measuredData"]["insideTemperature"]["dataPoints"]
    times = [t["timestamp"] for t in temperatures]
    values = [t["value"]["celsius"] for t in temperatures]
    _daily_data = pd.DataFrame(
        {
            "time": times,
            "temperature": values,
        }
    )
    _daily_data["time"] = pd.to_datetime(_daily_data["time"])
    _daily_data["temperature"] = _daily_data["temperature"].astype(float)
    return _daily_data


@read_jsonlist_write_parquet
def get_daily_targets(raw_row):
    targets = raw_row["settings"]["dataIntervals"]
    targets_selected = [c for c in targets if c["value"]["power"] == "ON"]
    starts = [t["from"] for t in targets_selected]
    ends = [t["to"] for t in targets_selected]
    values = [t["value"]["temperature"]["celsius"] for t in targets_selected]
    _daily_data = pd.DataFrame(
        {
            "start": starts,
            "end": ends,
            "temperature": values,
        }
    )
    _daily_data["start"] = pd.to_datetime(_daily_data["start"])
    _daily_data["end"] = pd.to_datetime(_daily_data["end"])
    _daily_data["temperature"] = _daily_data["temperature"].astype(float)
    return _daily_data


@read_jsonlist_write_parquet
def get_daily_intensity(raw_row):
    heat_name_to_value = {
        "NONE": 0,
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 3,
    }
    targets_selected = raw_row["callForHeat"]["dataIntervals"]
    starts = [t["from"] for t in targets_selected]
    ends = [t["to"] for t in targets_selected]
    values = [heat_name_to_value[t["value"]] for t in targets_selected]
    _daily_data = pd.DataFrame(
        {
            "start": starts,
            "end": ends,
            "intensity": values,
        }
    )
    _daily_data["start"] = pd.to_datetime(_daily_data["start"])
    _daily_data["end"] = pd.to_datetime(_daily_data["end"])
    _daily_data["intensity"] = _daily_data["intensity"].astype(int)
    return _daily_data


def ingest_raw_data(source_dir, destination_dir):
    print("\nCleaning data...")
    get_daily_temperature(
        source_dir, destination_dir, file_name_destination="temperatures"
    )
    get_daily_targets(source_dir, destination_dir, file_name_destination="targets")
    get_daily_intensity(source_dir, destination_dir, file_name_destination="intensity")
