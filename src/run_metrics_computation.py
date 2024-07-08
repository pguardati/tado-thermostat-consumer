import os
import pandas as pd
from datetime import datetime, timezone

import click

from src.common import read_parquet_write_parquet

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAKE_DIR = os.path.join(PROJECT_DIR, "data")


@read_parquet_write_parquet
def compute_metrics(temperatures, params):
    df = temperatures.copy()
    metrics = {}

    # plto time vs temp
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    ax.plot(df["time"], df["temperature"])
    ax.set_title("Temperature vs Time")
    plt.show()

    # TODO: aggregate before doing quality

    # Completeness - check nans and zeros
    metrics["missing_values"] = df.isnull().sum().to_dict()
    metrics["zero_values"] = (df == 0).sum().to_dict()

    # Consistency - check for consistent deltas
    time_diffs = df["time"].diff().dropna()
    metrics["time_differences"] = time_diffs.value_counts()

    # Accuracy - check for outliers
    temperature_stats = df["temperature"].describe()
    metrics["temperature_stats"] = temperature_stats

    lower_bound = temperature_stats["mean"] - 3 * temperature_stats["std"]
    upper_bound = temperature_stats["mean"] + 3 * temperature_stats["std"]
    anomalies = df[
        (df["temperature"] < lower_bound) | (df["temperature"] > upper_bound)
    ]
    metrics["anomalies"] = anomalies

    # Timeliness - check for delays
    now = datetime.now(timezone.utc)
    df["delay"] = (now - df["time"]).dt.total_seconds() / 3600  # Delay in hours
    metrics["delays"] = df[["time", "delay"]]

    # Uniqueness - check for duplicates
    duplicate_records = df[df.duplicated()]
    metrics["duplicate_records"] = duplicate_records

    # Integrity - check for correct data types
    data_types = df.dtypes
    metrics["data_types"] = data_types
    correct_format = pd.to_datetime(df["time"], errors="coerce").notnull().all()
    metrics["time_correct_format"] = correct_format

    _metrics = pd.to_datetime(metrics)
    # TODO: fix
    return _metrics


def main(
    lake_dir,
):
    silver_dir = os.path.join(lake_dir, "processed")
    compute_metrics(
        source_dir=silver_dir,
        destination_dir=silver_dir,
        file_name_source="temperatures",
        file_name_destination="temperatures_quality",
        settings=None,
    )


@click.command()
@click.option("--lake_dir", default=LAKE_DIR, help="Directory where to store the data")
def run_cli(**kwargs):
    main(**kwargs)


if __name__ == "__main__":
    run_cli()
