import os
import click

from src.extract import get_historic_data
from visualise import (
    _get_heat_commands,
    _get_temperatures,
    _plot_all_temperatures,
    _plot_overlapping_temperatures,
)


def plot_temperatures(
    download_dir,
    plot_all,
    plot_last_days,
):
    files = os.listdir(download_dir)
    _temperatures = _get_temperatures(files, download_dir)
    _commands = _get_heat_commands(files, download_dir)
    if plot_all:
        _plot_all_temperatures(_temperatures, _commands)
    if plot_last_days:
        _plot_overlapping_temperatures(_temperatures)


def main(
    start_date,
    download_dir,
    plot_all,
    plot_last_days,
):
    os.makedirs(download_dir, exist_ok=True)
    get_historic_data(start_date, download_dir)
    plot_temperatures(
        download_dir,
        plot_all=plot_all,
        plot_last_days=plot_last_days,
    )


@click.command()
@click.option("--start_date", default="2023-05-18", help="Start date for the data")
@click.option("--download_dir", default="data", help="Directory to download data to")
@click.option("--plot_all", default=True, help="Plot all temperatures")
@click.option(
    "--plot_last_days", default=False, help="Plot last 7 days of temperatures"
)
def run_cli(**kwargs):
    main(**kwargs)


if __name__ == "__main__":
    run_cli()
