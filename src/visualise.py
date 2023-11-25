import json
import os

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

# set interactive backend
plt.switch_backend("TkAgg")


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
    valid = [c for c in targets if c["value"]["power"] == "ON"]
    starts = [t["from"] for t in valid]
    ends = [t["to"] for t in valid]
    values = [t["value"]["temperature"]["celsius"] for t in valid]
    temperature_targets.append(
        pd.DataFrame(
            {
                "start": starts,
                "end": ends,
                "temperature": values,
            }
        )
    )


def _plot_all_temperatures(_temperatures, targets, start_date):
    def _preprocess_temperatures(df, _start_date):
        _df = df.copy()
        _df["time"] = pd.to_datetime(_df["time"])
        _df = _df.set_index("time")
        _df = _df[_df.index > _start_date]
        _df = _df.sort_values(by=["time"])
        return _df

    def _preprocess_commands(df, _start_date):
        # from start,end,value create a dataframe with time,temperature
        _df = df.copy()
        _df["start"] = pd.to_datetime(_df["start"])
        _df["end"] = pd.to_datetime(_df["end"])
        _temperature_ref = []
        for _, row in _df.iterrows():
            _temperature_ref.append(
                pd.DataFrame(
                    {
                        "time": pd.date_range(row["start"], row["end"], freq="H"),
                        "temperature": row["temperature"],
                    }
                )
            )
        _df2 = pd.concat(_temperature_ref)
        _df2 = _df2.sort_values(by=["time"])
        _df2 = _df2.set_index("time")
        _df2 = _df2[_df2.index > _start_date]
        return _df2

    def _plot(_t, _c):
        fig, ax = plt.subplots()
        ax.plot(_t.index, _t["temperature"], label="measured", color="blue")
        ax.plot(_c.index, _c["temperature"], label="commanded", color="red")
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d-%m"))
        plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator())
        plt.gcf().autofmt_xdate()
        plt.grid(True)
        plt.legend( loc='lower left') 
        plt.title(f"Living Room Temperatures since {_t.index.min().strftime('%Y-%m-%d')}")
        plt.show()

    _t = _preprocess_temperatures(_temperatures, start_date)
    _c = _preprocess_commands(targets, start_date)
    _plot(_t, _c)


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
