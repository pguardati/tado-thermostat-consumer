import unittest

import pandas as pd
from pathlib import Path

from src.cli.extract_and_process_thermostat import _run_transformations
from src.stages.storage import read_json_files
from src.stages.visualise import Granularity, _plot_view

OVERWRITE_EXPECTATIONS = False
current_file_path = Path(__name__).resolve()
test_dir = current_file_path.parent / "resources" / "test_etl"
path_view_expected = test_dir / "view_expected.parquet"
path_view_actual = test_dir / "view_actual_tmp.parquet"
staging_dir = test_dir / "staging"


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
        daily_tado_data = read_json_files(staging_dir)
        _view = _run_transformations(
            daily_tado_data,
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
