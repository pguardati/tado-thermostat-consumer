import os
from datetime import datetime, timedelta

import click
import pandas as pd

from src.stages.aggregate import generate_aggregate_view
from src.stages.backup import LocalBackup
from src.stages.clean import (
    clean_temperatures,
    clean_targets,
    clean_intensity,
    get_reference_dates,
)
from src.stages.extract import extract_files_from_tado_api, PARTITION_NAME
from src.stages.ingest import (
    get_daily_temperature,
    get_daily_targets,
    get_daily_intensity,
)
from src.stages.storage import read_json_files
from src.stages.visualise import (
    Granularity,
    _plot_view,
)

START_TIME = (datetime.now() - timedelta(days=550)).date()
PROJECT_NAME = "tado-thermostat-consumer"
REPOSITORY_PATH = os.path.realpath(__file__)[
    : os.path.realpath(__file__).find(PROJECT_NAME)
]
PROJECT_DIR = os.path.join(REPOSITORY_PATH, PROJECT_NAME)
LAKE_DIR = os.path.join(PROJECT_DIR, "data")


def _create_local_storage(lake_dir):
    backup_dir = os.path.join(lake_dir, "backups")
    staging_dir = os.path.join(lake_dir, "staging")
    os.makedirs(staging_dir, exist_ok=True)
    return backup_dir, staging_dir


def _run_transformations(
    daily_tado_data,
    start_date=None,
    end_date=None,
):
    _temperature_raw = pd.concat(
        [get_daily_temperature(data) for data in daily_tado_data]
    )
    _targets_raw = pd.concat([get_daily_targets(data) for data in daily_tado_data])
    _intensity_raw = pd.concat([get_daily_intensity(data) for data in daily_tado_data])

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


def main(
    start_date,
    lake_dir,
    plot_all,
    reload_today,
    reload_all,
    visual_granularity,
):
    backup_dir, staging_dir = _create_local_storage(lake_dir)

    backup_system = LocalBackup(target_dir=staging_dir, backup_dir=backup_dir)
    backup_system.restore_backup()

    extract_files_from_tado_api(start_date, staging_dir, reload_today, reload_all)

    daily_tado_data = read_json_files(staging_dir)
    _view = _run_transformations(
        daily_tado_data,
        start_date=start_date,
        end_date=None,
    )

    if plot_all:
        _plot_view(_view, visual_granularity)


@click.command()
@click.option("--start_date", default=START_TIME, help="Start date for the data")
@click.option("--lake_dir", default=LAKE_DIR, help="Directory where to store the data")
@click.option("--plot_all", default=True, help="Plot all temperatures")
@click.option("--reload_today", default=True, help="Reload today's data")
@click.option("--reload_all", default=False, help="Reload all data")
@click.option(
    "--visual-granularity",
    default=Granularity.MONTH,
    type=Granularity,
    help="Granularity of visualisation",
)
def run_cli(**kwargs):
    main(**kwargs)


if __name__ == "__main__":
    run_cli()
