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
    return dates


def clean_temperatures(
    temperatures,
    sample_time="5T",
):
    COLUMNS_INPUT = ["time", "temperature"]
    COLUMNS_OUTPUT = ["time", "time_raw", "temperature"]
    _t = temperatures.copy()

    _t = _t[COLUMNS_INPUT]
    _t["time"] = pd.to_datetime(_t["time"])

    _t["time_raw"] = _t["time"]
    _t_res = _t.set_index("time").resample(sample_time).mean()
    _t_res = _t_res.reset_index()
    _t_res["temperature"] = _t_res["temperature"].ffill()

    _t_clean = _t_res[COLUMNS_OUTPUT]
    return _t_clean
