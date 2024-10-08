from datetime import datetime

import pandas as pd


def get_master_dates(start_date, days=90):
    start_date = pd.to_datetime(start_date)
    end_date = start_date + pd.DateOffset(days=days)
    dates = pd.date_range(start_date, end_date, freq="5T")
    _dates = pd.DataFrame(dates, columns=["time"])
    return dates


def aggregate_temperatures_new(df, dates):
    # TODO: resample and merge on date
    pass
