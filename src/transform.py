import json
import os

import pandas as pd


def read_daily_temperature(_temperatures, download_dir, file):
    with open(os.path.join(download_dir, file), "r") as f:
        historic_data = json.load(f)
    temperatures = historic_data["measuredData"]["insideTemperature"]["dataPoints"]
    times = [t["timestamp"] for t in temperatures]
    values = [t["value"]["celsius"] for t in temperatures]
    _temperatures.append(
        pd.DataFrame(
            {
                "time": times,
                "temperature": values,
            }
        )
    )


def read_daily_targets(temperature_targets, download_dir, file):
    with open(os.path.join(download_dir, file), "r") as f:
        historic_data = json.load(f)
    targets = historic_data["settings"]["dataIntervals"]
    targets_selected = [c for c in targets if c["value"]["power"] == "ON"]
    starts = [t["from"] for t in targets_selected]
    ends = [t["to"] for t in targets_selected]
    values = [t["value"]["temperature"]["celsius"] for t in targets_selected]
    temperature_targets.append(
        pd.DataFrame(
            {
                "start": starts,
                "end": ends,
                "temperature": values,
            }
        )
    )


def read_daily_intensity(heaters_intensity, download_dir, file):
    heat_name_to_value = {
        "NONE": 0,
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 3,
    }
    with open(os.path.join(download_dir, file), "r") as f:
        historic_data = json.load(f)
    targets_selected = historic_data["callForHeat"]["dataIntervals"]
    starts = [t["from"] for t in targets_selected]
    ends = [t["to"] for t in targets_selected]
    values = [heat_name_to_value[t["value"]] for t in targets_selected]
    heaters_intensity.append(
        pd.DataFrame(
            {
                "start": starts,
                "end": ends,
                "intensity": values,
            }
        )
    )


def _get_temperatures(files, download_dir):
    daily_temperatures = []
    for file in files:
        read_daily_temperature(daily_temperatures, download_dir, file)
    _temperatures = pd.concat(daily_temperatures)
    return _temperatures


def _get_temperature_targets(files, download_dir):
    temperature_targets = []
    for file in files:
        read_daily_targets(
            temperature_targets,
            download_dir,
            file,
        )
    _commands = pd.concat(temperature_targets)
    return _commands


def _get_heaters_intensity(files, download_dir):
    heaters_intensity = []
    for file in files:
        read_daily_intensity(
            heaters_intensity,
            download_dir,
            file,
        )
    _commands = pd.concat(heaters_intensity)
    return _commands
