import os
import json
import pandas as pd
import matplotlib.pyplot as plt

# set interactive backend
plt.switch_backend("TkAgg")


def read_daily_temperature(_temperatures, download_dir, file):
    with open(os.path.join(download_dir, file), "r") as f:
        historic_data = json.load(f)
    temperatures = historic_data["measuredData"]["insideTemperature"][
        "dataPoints"]
    times = [t["timestamp"] for t in temperatures]
    values = [t["value"]["celsius"] for t in temperatures]
    _temperatures.append(pd.DataFrame({"time": times, "temperature": values}))


def _plot_all_temperatures(df):
    df["time"] = pd.to_datetime(df["time"])
    df = df.set_index("time")
    df = df.resample("H").mean()
    df.plot()
    most_recent_date = df.index.min().strftime("%Y-%m-%d")
    plt.title(f"Living Room Temperatures since {most_recent_date}")
    plt.legend().remove()
    plt.show()


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


def plot_temperatures(download_dir):
    files = os.listdir(download_dir)
    _temperatures = _get_temperatures(files, download_dir)
    _plot_all_temperatures(_temperatures)
    _plot_overlapping_temperatures(_temperatures)
