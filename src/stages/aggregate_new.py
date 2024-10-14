from datetime import datetime

import pandas as pd


def get_master_dates(
    start_date,
    sample_time="5T",
    days=90,
):
    start_date = pd.to_datetime(start_date)
    end_date = start_date + pd.DateOffset(days=days)
    dates = pd.date_range(start_date, end_date, freq=sample_time)
    _dates = pd.DataFrame(dates, columns=["time"])
    return _dates


def clean_temperatures(
    temperatures,
    sample_time="5T",
):
    _t = temperatures.copy()[["time", "temperature"]]
    _t["time"] = pd.to_datetime(_t["time"])

    _t["time_raw"] = _t["time"]
    _t_res = _t.set_index("time").resample(sample_time).mean()
    _t_res = _t_res.reset_index()
    _t_res["temperature"] = _t_res["temperature"].ffill()

    _t_clean = _t_res[["time", "time_raw", "temperature"]]
    return _t_clean


def generate_view(_temperature, _dates):
    _t = _temperature.copy()[["time", "time_raw", "temperature"]]
    _d = _dates.copy()[["time"]]

