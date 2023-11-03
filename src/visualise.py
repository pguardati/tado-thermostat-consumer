import os
import json
import pandas as pd
import matplotlib.pyplot as plt

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


def read_daily_commands(heat_commands, download_dir, file):
    with open(os.path.join(download_dir, file), "r") as f:
        historic_data = json.load(f)
    commands = historic_data["settings"]["dataIntervals"]
    valid_commands = [c for c in commands if c["value"]["power"] == "ON"]
    command_starts = [t["from"] for t in valid_commands]
    command_ends = [t["to"] for t in valid_commands]
    command_values = [t["value"]["temperature"]["celsius"] for t in valid_commands]
    heat_commands.append(
        pd.DataFrame(
            {
                "start": command_starts,
                "end": command_ends,
                "temperature": command_values,
            }
        )
    )


def _plot_all_temperatures(_temperatures, commmands):
    def _preprocess_temperatures(df):
        _df = df.copy()
        _df["time"] = pd.to_datetime(_df["time"])
        _df = _df.set_index("time")
        _df = _df.resample("H").mean()
        return _df

    def _preprocess_commands(df):
        # from start,end,value create a datafram with time,temperature
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
        return _df2

    def _plot(_t, _c):
        fig, ax = plt.subplots()
        ax.plot(_t.index, _t["temperature"], label="measured", color="blue")
        ax.plot(_c.index, _c["temperature"], label="commanded", color="red")
        most_recent_date = _t.index.min().strftime("%Y-%m-%d")
        plt.title(f"Living Room Temperatures since {most_recent_date}")
        plt.legend()
        plt.show()

    _t = _preprocess_temperatures(_temperatures)
    _c = _preprocess_commands(commmands)
    _plot(_t, _c)


def _plot_overlapping_temperatures(df_raw):
    # plot the daily temperatures on top of each other
    df = df_raw.copy()
    # parse datetime
    df["datetime"] = pd.to_datetime(df["time"])
    # get last 7 days
    df = df[df["datetime"] > df["datetime"].max() - pd.Timedelta(days=7)]
    # get day of the year
    df["day"] = df["datetime"].dt.date
    df["day"] = pd.to_datetime(df["day"])
    df["day"] = df["day"].dt.dayofyear
    # get hour
    df["time"] = df["datetime"].dt.hour
    # drop duplicates of date and time
    df = df.sort_values(by=["day", "time"])
    df = df.drop_duplicates(subset=["day", "time"])
    df = df.dropna()
    for day in df["day"].unique():
        df_day = df[df["day"] == day]
        plt.plot(df_day["time"], df_day["temperature"])
    plt.legend(df["day"].unique())
    plt.title("Daily Temperatures over the last 7 days")
    plt.show()


def _get_temperatures(files, download_dir):
    daily_temperatures = []
    for file in files:
        read_daily_temperature(daily_temperatures, download_dir, file)
    _temperatures = pd.concat(daily_temperatures)
    return _temperatures


def _get_heat_commands(files, download_dir):
    heat_commands = []
    for file in files:
        read_daily_commands(
            heat_commands,
            download_dir,
            file,
        )
    _commands = pd.concat(heat_commands)
    return _commands

