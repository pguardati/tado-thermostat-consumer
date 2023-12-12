import os
from datetime import datetime, timedelta

import click

from src.extract import get_historic_data
from src.visualise import _plot_all_temperatures
from transform import (
    _get_heaters_intensity,
    _get_temperature_targets,
    _get_temperatures,
)

ONE_WEEK_AGO = (datetime.now() - timedelta(days=10)).date()
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOWNLOAD_DIR = os.path.join(PROJECT_DIR, "data")


def plot_temperatures(
    download_dir,
    start_date,
    plot_all,
):
    files = os.listdir(download_dir)
    _temperatures = _get_temperatures(files, download_dir)
    _targets = _get_temperature_targets(files, download_dir)
    _heaters_intensity = _get_heaters_intensity(files, download_dir)
    if plot_all:
        _plot_all_temperatures(
            _temperatures,
            _targets,
            _heaters_intensity,
            start_date,
        )


def main(
    start_date,
    download_dir,
    plot_all,
    reload_today,
    reload_all,
):
    os.makedirs(download_dir, exist_ok=True)
    get_historic_data(start_date, download_dir, reload_today, reload_all)
    plot_temperatures(
        download_dir,
        start_date=start_date,
        plot_all=plot_all,
    )


@click.command()
@click.option("--start_date", default=ONE_WEEK_AGO, help="Start date for the data")
@click.option(
    "--download_dir", default=DOWNLOAD_DIR, help="Directory to download data to"
)
@click.option("--plot_all", default=True, help="Plot all temperatures")
@click.option("--reload_today", default=True, help="Reload today's data")
@click.option("--reload_all", default=True, help="Reload all data")
def run_cli(**kwargs):
    main(**kwargs)


if __name__ == "__main__":
    run_cli()
