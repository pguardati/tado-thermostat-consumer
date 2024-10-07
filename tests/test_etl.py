import pandas as pd
from pathlib import Path

from src.common import read_json_files
from src.stages.aggregate import (
    aggregate_intensity,
    aggregate_targets,
    aggregate_temperatures,
)
from src.stages.ingest import (
    get_daily_intensity,
    get_daily_targets,
    get_daily_temperature,
)
from src.visualise import plot_aggregates

current_file_path = Path(__name__).resolve()
test_dir = current_file_path.parent / "resources" / "test_etl"
staging_dir = test_dir / "staging"


def _run_serial_etl(staging_dir):
    raw_row = read_json_files(staging_dir)

    _intensity_raw = pd.concat([get_daily_intensity(data) for data in raw_row])
    _targets_raw = pd.concat([get_daily_targets(data) for data in raw_row])
    _temperature_raw = pd.concat([get_daily_temperature(data) for data in raw_row])

    _intensity_agg = aggregate_intensity(
        _intensity_raw,
        {"start_date": "2023-11-21"},
    )
    _targets_agg = aggregate_targets(
        _targets_raw,
        {"start_date": "2023-11-21"},
    )
    _temperature_agg = aggregate_temperatures(
        _temperature_raw,
        {"start_date": "2023-11-21"},
    )
    return _temperature_agg, _targets_agg, _intensity_agg


def test_etl():
    _temperature, _targets, _intensity = _run_serial_etl(staging_dir)
