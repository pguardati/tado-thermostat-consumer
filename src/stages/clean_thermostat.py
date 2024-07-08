import os
from datetime import datetime

import pandas as pd

from src.common import read_parquet_write_parquet


def resample(df, granularity="10T", time_column="time"):
    _df = df.copy()
    _df[time_column] = _df[time_column] + pd.to_timedelta(
        _df.groupby(time_column).cumcount(), unit="ms"
    )
    _df = _df.set_index(time_column).resample(granularity).ffill().reset_index()
    return _df


@read_parquet_write_parquet
def clean_temperatures(df, params):
    columns = [
        "time",
        "temperature",
    ]
    _df = df.copy()
    _start_date = params["start_date"]

    _df = _df[_df["time"] > _start_date]

    _df = resample(_df)
    _df = _df.sort_values(by=["time"])
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

    _df2 = resample(_df2)
    _df2 = _df2.sort_values(by=["time"])
    _df2 = _df2[columns]
    return _df2


@read_parquet_write_parquet
def clean_intensity(df, params):
    columns = [
        "time",
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

    _df2 = resample(_df2)
    _df2 = _df2.sort_values(by=["time"])
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
