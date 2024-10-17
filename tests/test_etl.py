import unittest

import pandas as pd
from pathlib import Path

from src.stages.extract import PARTITION_NAME
from src.stages.storage import read_json_files

from src.stages.aggregate import (
    generate_aggregate_view,
)
from src.stages.clean import (
    get_reference_dates,
    clean_temperatures,
    clean_targets,
    clean_intensity,
)
from src.stages.ingest import (
    get_daily_intensity,
    get_daily_targets,
    get_daily_temperature,
)
from src.stages.visualise import Granularity, _plot_view

OVERWRITE_EXPECTATIONS = False
current_file_path = Path(__name__).resolve()
test_dir = current_file_path.parent / "resources" / "test_etl"
path_view_expected = test_dir / "view_expected.parquet"
path_view_actual = test_dir / "view_actual_tmp.parquet"
staging_dir = test_dir / "staging"


def _run_serial_new_etl(
    staging_dir,
    start_date=None,
    end_date=None,
):
    raw_row = read_json_files(staging_dir)

    _temperature_raw = pd.concat([get_daily_temperature(data) for data in raw_row])
    _targets_raw = pd.concat([get_daily_targets(data) for data in raw_row])
    _intensity_raw = pd.concat([get_daily_intensity(data) for data in raw_row])

    _temperature_clean = clean_temperatures(_temperature_raw)
    _targets_clean = clean_targets(_targets_raw)
    _intensity_clean = clean_intensity(_intensity_raw)

    _time = _temperature_clean["time"]
    _start_date = start_date or _time.min().date().strftime(PARTITION_NAME)
    _end_date = end_date or _time.max().date().strftime(PARTITION_NAME)
    _dates = get_reference_dates(_start_date, _end_date)

    _view = generate_aggregate_view(
        _dates,
        _temperature_clean,
        _targets_clean,
        _intensity_clean,
    )
    return _view


def write_test_dataframes(
    df,
    path_actual,
    path_expected,
    overwrite=False,
):
    if overwrite:
        df.to_parquet(path_expected)

    df.to_parquet(path_actual)


def compare_test_dataframes(
    path_actual,
    path_expected,
):
    _view_actual = pd.read_parquet(path_actual)
    _view_expected = pd.read_parquet(path_expected)
    pd.testing.assert_frame_equal(_view_actual, _view_expected)


class TestLocalBackup(unittest.TestCase):
    def test_new_etl(self, plot=True):
        _view = _run_serial_new_etl(
            staging_dir,
            start_date="2024-03-01",
            end_date="2024-03-31",
        )
        write_test_dataframes(
            _view,
            path_view_actual,
            path_view_expected,
            overwrite=OVERWRITE_EXPECTATIONS,
        )
        compare_test_dataframes(
            path_view_actual,
            path_view_expected,
        )

        if plot:
            _plot_view(_view, Granularity.MONTH)
