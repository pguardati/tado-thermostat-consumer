from datetime import datetime

import pandas as pd


def get_master_dates(
    start_date,
    sample_time="5T",
    days=90,
):
    start_date = pd.to_datetime(start_date, utc=True)

    end_date = start_date + pd.DateOffset(days=days)
    dates = pd.date_range(start_date, end_date, freq=sample_time)
    _dates = pd.DataFrame(dates, columns=["time"])

    _dates = _dates[["time"]]
    return _dates


def clean_temperatures(
    temperatures,
    sample_time="5T",
):
    _t = temperatures.copy()[["time", "temperature"]]
    _t["time"] = pd.to_datetime(_t["time"], utc=True)

    # resample, but keep the raw time
    _t["time_raw"] = _t["time"]
    _t_res = _t.set_index("time").resample(sample_time).mean()
    _t_res = _t_res.reset_index()
    _t_res = _t_res.ffill()

    _t_res["value"] = _t_res["temperature"]
    _t_clean = _t_res[["time", "time_raw", "value"]]
    return _t_clean


def clean_targets(
    intensity,
    sample_time="5T",
):
    pass


def generate_view(_temperature, _dates):
    _t = _temperature.copy()[["time", "time_raw", "value"]]
    _d = _dates.copy()[["time"]]

    _view = pd.merge(_d, _t, on="time", how="left")
    _view = _view.rename(
        columns={
            "value": "temperature_value",
            "time_raw": "temperature_time_raw",
        },
    )

    _view = _view.fillna(method="ffill")
    _view = _view.fillna(method="bfill")
    _view = _view[
        [
            "time",
            "temperature_value",
            "temperature_time_raw",
        ]
    ]
    return _view
