import os

import click

from src.extract import get_historic_data
from visualise import _get_heat_commands, _get_temperatures, _plot_all_temperatures


def plot_temperatures(
    download_dir,
    start_date,
    plot_all,
):
    files = os.listdir(download_dir)
    _temperatures = _get_temperatures(files, download_dir)
    _commands = _get_heat_commands(files, download_dir)
    if plot_all:
        _plot_all_temperatures(_temperatures, _commands, start_date)


def main(
    start_date,
    download_dir,
    plot_all,
    reload_today,
):
    os.makedirs(download_dir, exist_ok=True)
    get_historic_data(start_date, download_dir, reload_today)
    plot_temperatures(
        download_dir,
        start_date=start_date,
        plot_all=plot_all,
    )


@click.command()
@click.option("--start_date", default="2023-05-18", help="Start date for the data")
@click.option("--download_dir", default="data", help="Directory to download data to")
@click.option("--plot_all", default=True, help="Plot all temperatures")
@click.option("--reload_today", default=False, help="Reload today's data")
def run_cli(**kwargs):
    main(**kwargs)


if __name__ == "__main__":
    run_cli()
