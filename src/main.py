import os
from datetime import datetime, timedelta

import click
from src.stages.extract import extract_files_from_tado_api
from src.visualise import (
    plot_aggregates,
    Granularity,
)
from src.stages.ingest import ingest_raw_data
from src.stages.aggregate import clean_data

ONE_WEEK_AGO = (datetime.now() - timedelta(days=100)).date()
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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

    ingest_raw_data(staging_dir, bronze_dir)
    clean_data(bronze_dir, silver_dir, start_date)

    if plot_all:
        plot_aggregates(silver_dir, visual_granularity)


@click.command()
@click.option("--start_date", default=ONE_WEEK_AGO, help="Start date for the data")
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
