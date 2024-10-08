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

    # extract squares from points
    _df = _df.sort_values(by=["start"])
    _targets_ref = []
    for i, row in _df.iterrows():
        _targets_ref.append(
            {
                "id": i,
                "time": row["start"],
                "temperature": row["temperature"],
            }
        )
        _targets_ref.append(
            {
                "id": i,
                "time": row["end"],
                "temperature": row["temperature"],
            }
        )
    _df2 = pd.DataFrame(_targets_ref)

    # sort
    _df2 = _df2.sort_values(by=["time", "id"])

    # output schema validation
    _df2["time"] = pd.to_datetime(_df2["time"])
    return _df2


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


