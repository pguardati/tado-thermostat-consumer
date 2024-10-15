import pandas as pd


def _resample(df, sample_time):
    """resample, but keep the raw sensing time"""
    df["time_raw"] = df["time"]
    _df_res = df.set_index("time").resample(sample_time).mean()
    _df_res = _df_res.reset_index()
    _df_res = _df_res.ffill()
    return _df_res


def _extract_target_changes(targets, value_column="temperature"):
    targets_changes = []
    for i, row in targets.iterrows():
        targets_changes.append(
            {
                "time": row["start"],
                value_column: row[value_column],
            }
        )
    _tc = pd.DataFrame(targets_changes)

    _tc = _tc.sort_values(by=["time"]).reset_index(drop=True)
    _tc = _tc.drop_duplicates(subset=["time"], keep="first")
    return _tc


def get_reference_dates(
    start_date,
    end_date,
    sample_time="5T",
):
    start_date = pd.to_datetime(start_date, utc=True)
    end_date = pd.to_datetime(end_date, utc=True)

    dates = pd.date_range(start_date, end_date, freq=sample_time)
    _dates = pd.DataFrame(dates, columns=["time"])

    _dates = _dates[["time"]]
    return _dates


def clean_temperatures(
    temperatures,
    sample_time="5T",
):
    _t = temperatures.copy()[["time", "temperature"]]
    _t["time"] = pd.to_datetime(_t["time"], utc=True)

    _t_res = _resample(_t, sample_time)

    _t_res["value"] = _t_res["temperature"]
    _t_clean = _t_res[["time", "time_raw", "value"]]
    return _t_clean


def clean_targets(
    targets,
    sample_time="5T",
):
    _t = targets.copy()[["start", "end", "temperature"]]
    _t["start"] = pd.to_datetime(_t["start"], utc=True)

    _tc = _extract_target_changes(_t, value_column="temperature")
    _tcr = _resample(_tc, sample_time)

    _tcr["value"] = _tcr["temperature"]
    _t_clean = _tcr[["time", "time_raw", "value"]]
    return _t_clean


def clean_intensity(
    intensity,
    sample_time="5T",
):
    _i = intensity.copy()[["start", "end", "intensity"]]
    _i["start"] = pd.to_datetime(_i["start"], utc=True)

    _ic = _extract_target_changes(_i, value_column="intensity")
    _icr = _resample(_ic, sample_time)

    _icr["value"] = _icr["intensity"]
    _i_clean = _icr[["time", "time_raw", "value"]]
    return _i_clean
