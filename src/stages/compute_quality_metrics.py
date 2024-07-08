import pandas as pd
from datetime import datetime, timezone
from src.common import read_parquet_write_parquet


@read_parquet_write_parquet
def compute_data_freshness(temperatures, params):
    df = temperatures.copy()
    metrics = {}

    # Completeness - check nans and zeros
    metrics["missing_values"] = df.isnull().sum()

    # Consistency - check for consisten deltas
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


def compute_quality_metrics(silver_dir):
    # for now, only on temperatures
    compute_data_freshness(
        source_dir=silver_dir,
        destination_dir=silver_dir,
        file_name_source="temperatures",
        file_name_destination="temperatures_quality",
        settings=None,
    )
