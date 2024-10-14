from datetime import datetime

import pandas as pd


def aggregate_temperatures(df, params):
    _df = df.copy()
    _start_date = params["start_date"]

    # input schema validation
    df["time"] = pd.to_datetime(df["time"])

    # filter
    _df = _df[_df["time"] > _start_date]

    # sort
    _df = _df.sort_values(by=["time"])

    # output schema validation
    _df["time"] = pd.to_datetime(_df["time"])
    return _df


def aggregate_targets(df, params):
    _df = df.copy()
    _start_date = pd.to_datetime(params["start_date"], utc=True)

    # input schema validation
    df["start"] = pd.to_datetime(df["start"], utc=True)

    # filter
    _df = _df[_df["start"] > _start_date]

    # get reference changes
    _targets_ref = []
    for i, row in df.iterrows():
        _targets_ref.append({"time": row["start"], "temperature": row["temperature"]})
    _t1 = pd.DataFrame(_targets_ref)
    _t1 = _t1.sort_values(by=["time"]).reset_index(drop=True)
    _t1 = _t1.drop_duplicates(subset=["time"], keep="first")

    # resample
    _t1["time_raw"] = _t1["time"]
    _t1_res = _t1.set_index("time").resample("5T").mean().reset_index()
    _t1_res = _t1_res.ffill()
    return _t1_res


def aggregate_intensity(df, params):
    _df = df.copy()
    _start_date = params["start_date"]

    # input schema validation
    df["start"] = pd.to_datetime(df["start"])

    # filter
    bigger_than_start_date = _df["start"] > _start_date
    after_heaters_on = _df["start"] > datetime(2023, 11, 21).date().isoformat()
    _df = _df[bigger_than_start_date & after_heaters_on]

    # extract squares from points
    _df = _df.sort_values(by=["start"])
    _intensity_ref = []
    for i, row in _df.iterrows():
        _intensity_ref.append(
            {
                "id": i,
                "time": row["start"],
                "intensity": row["intensity"],
            }
        )
        _intensity_ref.append(
            {
                "id": i,
                "time": row["end"],
                "intensity": row["intensity"],
            }
        )
    _df2 = pd.DataFrame(_intensity_ref)

    # sort
    _df2 = _df2.sort_values(by=["time", "id"])

    # output schema validation
    _df2["time"] = pd.to_datetime(_df2["time"])
    return _df2
