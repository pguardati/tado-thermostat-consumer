from datetime import datetime

import pandas as pd


def aggregate_temperatures(df, params):
    _df = df.copy()
    _start_date = params["start_date"]

    _df = _df.set_index("time")
    _df = _df[_df.index > _start_date]
    _df = _df.sort_values(by=["time"])
    return _df


def aggregate_targets(df, params):
    _df = df.copy()
    _start_date = params["start_date"]

    _df = _df.sort_values(by=["start"])
    bigger_than_start_date = _df["start"] > _start_date
    _df = _df[bigger_than_start_date]
    _df = _df.reset_index(drop=True)
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
    _df2 = _df2.sort_values(by=["time", "id"])
    _df2 = _df2.set_index("time")
    return _df2


def aggregate_intensity(df, params):
    _df = df.copy()
    _start_date = params["start_date"]

    _df = _df.sort_values(by=["start"])
    bigger_than_start_date = _df["start"] > _start_date
    after_heaters_on = _df["start"] > datetime(2023, 11, 21).date().isoformat()
    _df = _df[bigger_than_start_date & after_heaters_on]
    _df = _df.reset_index(drop=True)
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
    _df2 = _df2.sort_values(by=["time", "id"])
    _df2 = _df2.set_index("time")
    return _df2


