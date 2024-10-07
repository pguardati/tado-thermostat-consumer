import pandas as pd


def generate_aggregate_view(
    _dates,
    _temperature,
    _targets,
    _intensity,
):
    _d = _dates.copy()[["time"]]
    _t = _temperature.copy()[["time", "time_raw", "value"]]
    _tr = _targets.copy()[["time", "time_raw", "value"]]
    _i = _intensity.copy()[["time", "time_raw", "value"]]

    # merge temperatures
    _view = pd.merge(_d, _t, on="time", how="left")
    _view = _view.rename(
        columns={
            "value": "temperature_value",
            "time_raw": "temperature_time_raw",
        },
    )

    # merge targets
    _view = pd.merge(_view, _tr, on="time", how="left")
    _view = _view.rename(
        columns={
            "value": "target_value",
            "time_raw": "target_time_raw",
        },
    )

    # merge intensity
    _view = pd.merge(_view, _i, on="time", how="left")
    _view = _view.rename(
        columns={
            "value": "intensity_value",
            "time_raw": "intensity_time_raw",
        },
    )

    _view = _view.ffill()
    _view = _view.bfill()
    _view = _view[
        [
            "time",
            "temperature_value",
            "temperature_time_raw",
            "target_value",
            "target_time_raw",
            "intensity_value",
            "intensity_time_raw",
        ]
    ]
    return _view
