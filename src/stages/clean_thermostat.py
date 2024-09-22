import os
from datetime import datetime

import pandas as pd

from src.common import read_parquet_write_parquet


@read_parquet_write_parquet
def clean_temperatures(df, params):
    columns = [
        "time",
        "temperature",
    ]
    _df = df.copy()
    _start_date = params["start_date"]

    _df = _df.set_index("time")
    _df = _df[_df.index > _start_date]
    _df = _df.sort_values(by=["time"])

    _df = _df.reset_index()
    _df = _df[columns]
    return _df


@read_parquet_write_parquet
def clean_targets(df, params):
    columns = [
        "time",
        "temperature",
    ]
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
    _df2 = pd.DataFrame(_targets_ref) if _targets_ref else pd.DataFrame(columns=columns)

    # TODO: unify key and resample
    # add cumulative delta to time to deduplicate
    # _df2["time"] = _df2["time"] + pd.to_timedelta(
    #     _df2.groupby("time").cumcount(), unit="ms"
    # )
    # # resample each minute
    # _df2 = _df2.set_index("time")
    # _df2 = _df2.resample("1T").ffill()
    # _df2 = _df2.reset_index()
    # # plot - there is something like this in the original code
    # import matplotlib.pyplot as plt
    #
    # fig, ax = plt.subplots()
    # ax.plot(_df2["time"], _df2["temperature"], label="target", color="red", marker="o")
    # ax.set_title("Targets")
    # plt.show()

    _df2 = _df2.sort_values(by=["time"])
    _df2 = _df2[columns]
    return _df2


@read_parquet_write_parquet
def clean_intensity(df, params):
    columns = [
        "time",
        "id",
        "intensity",
    ]
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
    _df2 = (
        pd.DataFrame(_intensity_ref)
        if _intensity_ref
        else pd.DataFrame(columns=columns)
    )
    _df2 = _df2.sort_values(
        by=[
            "time",
            "id",
        ]
    )
    _df2 = _df2[columns]
    return _df2


# Usage
def clean_thermostat_data(source_dir, destination_dir, start_date):
    print("\nClean thermostat data...")
    params = {"start_date": start_date}
    clean_temperatures(
        source_dir, destination_dir, "temperatures", "temperatures", params
    )
    clean_targets(source_dir, destination_dir, "targets", "targets", params)
    clean_intensity(source_dir, destination_dir, "intensity", "intensity", params)
