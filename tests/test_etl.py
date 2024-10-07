import pandas as pd
from pathlib import Path

from src.common import read_json_files
from src.stages.ingest import get_daily_intensity
from src.visualise import plot_aggregates

current_file_path = Path(__name__).resolve()
test_dir = current_file_path.parent / "resources" / "test_etl"
staging_dir = test_dir / "staging"


def _run_serial_etl(staging_dir):
    raw_row = read_json_files(staging_dir)
    _processed = pd.concat([get_daily_intensity(data) for data in raw_row])


def test_etl():
    _temperature, _targets, _intensity = _run_serial_etl(staging_dir)
