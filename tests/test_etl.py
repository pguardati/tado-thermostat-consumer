import pandas as pd
from pathlib import Path

from src.common import read_json_files
from src.stages.aggregate import (
    aggregate_intensity,
    aggregate_targets,
    aggregate_temperatures,
)
from src.stages.aggregate_new import get_master_dates, aggregate_temperatures_new
from src.stages.ingest import (
    get_daily_intensity,
    get_daily_targets,
    get_daily_temperature,
)
from src.stages.visualise import _plot_aggregates, Granularity, _plot_temperatures

current_file_path = Path(__name__).resolve()
test_dir = current_file_path.parent / "resources" / "test_etl"
staging_dir = test_dir / "staging"


def _run_serial_legacy_etl(staging_dir):
    start_date = {"start_date": "2023-11-21"}
    raw_row = read_json_files(staging_dir)

    _temperature_raw = pd.concat([get_daily_temperature(data) for data in raw_row])
    _targets_raw = pd.concat([get_daily_targets(data) for data in raw_row])
    _intensity_raw = pd.concat([get_daily_intensity(data) for data in raw_row])

    _temperature_agg = aggregate_temperatures(_temperature_raw, start_date)
    _targets_agg = aggregate_targets(_targets_raw, start_date)
    _intensity_agg = aggregate_intensity(_intensity_raw, start_date)

    return _temperature_agg, _targets_agg, _intensity_agg


def test_legacy_etl():
    _temperature, _targets, _intensity = _run_serial_legacy_etl(staging_dir)
    _plot_aggregates(_temperature, _targets, _intensity, Granularity.MONTH)


def _run_serial_new_etl(staging_dir):
    start_date = {"start_date": "2023-11-21"}
    raw_row = read_json_files(staging_dir)

    _temperature_raw = pd.concat([get_daily_temperature(data) for data in raw_row])
    _targets_raw = pd.concat([get_daily_targets(data) for data in raw_row])
    _intensity_raw = pd.concat([get_daily_intensity(data) for data in raw_row])

    _dates = get_master_dates(start_date["start_date"])
    _temperature_agg = aggregate_temperatures_new(_temperature_raw, _dates)
    _targets_agg = None
    _intensity_agg = None

    return _temperature_agg, _targets_agg, _intensity_agg


def test_new_etl():
    _temperature, _targets, _intensity = _run_serial_new_etl(staging_dir)
    _plot_temperatures(_temperature, Granularity.MONTH)
