import os

from src.extract import get_historic_data
from src.visualise import plot_temperatures


def main(start_date, download_dir):
    os.makedirs(download_dir, exist_ok=True)
    get_historic_data(start_date, download_dir)
    plot_temperatures(download_dir)


if __name__ == "__main__":
    start_date = "2023-05-18"
    download_dir = "data"
    main(start_date, download_dir)
