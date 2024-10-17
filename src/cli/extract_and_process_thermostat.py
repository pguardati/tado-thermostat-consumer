import os
from datetime import datetime, timedelta

import click
from src.stages.extract import extract_files_from_tado_api
from src.stages.visualise import (
    Granularity,
    _plot_view,
)
from tests.test_etl import _run_serial_new_etl

START_TIME = (datetime.now() - timedelta(days=510)).date()
PROJECT_NAME = "tado-thermostat-consumer"
REPOSITORY_PATH = os.path.realpath(__file__)[
    : os.path.realpath(__file__).find(PROJECT_NAME)
]
PROJECT_DIR = os.path.join(REPOSITORY_PATH, PROJECT_NAME)
LAKE_DIR = os.path.join(PROJECT_DIR, "data")


def main(
    start_date,
    lake_dir,
    plot_all,
    reload_today,
    reload_all,
    visual_granularity,
):
    staging_dir = os.path.join(lake_dir, "staging")
    bronze_dir = os.path.join(lake_dir, "raw")
    silver_dir = os.path.join(lake_dir, "processed")
    for layer_dir in [staging_dir, bronze_dir, silver_dir]:
        os.makedirs(layer_dir, exist_ok=True)

    extract_files_from_tado_api(start_date, staging_dir, reload_today, reload_all)
    _view = _run_serial_new_etl(
        staging_dir,
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
