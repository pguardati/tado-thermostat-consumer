import pandas as pd
from pathlib import Path

from src.common import read_json_files

from src.stages.aggregate_new import (
    get_master_dates,
    clean_temperatures,
    generate_view,
    clean_targets,
)
from src.stages.ingest import (
    get_daily_intensity,
    get_daily_targets,
    get_daily_temperature,
)
from src.stages.visualise import _plot_aggregates, Granularity, _plot_temperatures

current_file_path = Path(__name__).resolve()
test_dir = current_file_path.parent / "resources" / "test_etl"
staging_dir = test_dir / "staging"


def _run_serial_new_etl(staging_dir):
    start_date = {"start_date": "2024-03-01"}
    raw_row = read_json_files(staging_dir)

    _temperature_raw = pd.concat([get_daily_temperature(data) for data in raw_row])
    _targets_raw = pd.concat([get_daily_targets(data) for data in raw_row])
    _intensity_raw = pd.concat([get_daily_intensity(data) for data in raw_row])

    _temperature_agg = clean_temperatures(_temperature_raw)
    _targets_agg = clean_targets(_targets_raw)
    _intensity_agg = None

    _dates = get_master_dates(start_date["start_date"])
    _view = generate_view(_temperature_agg, _targets_agg, _dates)

    return _view


def test_new_etl():
    _view = _run_serial_new_etl(staging_dir)
    _plot_temperatures(_view, Granularity.MONTH)
