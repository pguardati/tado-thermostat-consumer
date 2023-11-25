from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

plt.switch_backend("TkAgg")


def _preprocess_temperatures(df, _start_date):
    _df = df.copy()
    _df["time"] = pd.to_datetime(_df["time"])
    _df = _df.set_index("time")
    _df = _df[_df.index > _start_date]
    _df = _df.sort_values(by=["time"])
    return _df


def _preprocess_targets(df, _start_date):
    # from start,end,value create a dataframe with time,temperature
    _df = df.copy()
    _df["start"] = pd.to_datetime(_df["start"])
    _df["end"] = pd.to_datetime(_df["end"])
    _df = _df.sort_values(by=["start"])
    bigger_than_start_date = _df["start"] > _start_date
    _df = _df[bigger_than_start_date]
    _df = _df.reset_index(drop=True)
    _targets_ref = []
    for i, row in _df.iterrows():
        _targets_ref.append(
            {
                "id": i,
                "time": row["start"],
                "temperature": row["temperature"],
            }
        )
        _targets_ref.append(
            {
                "id": i,
                "time": row["end"],
                "temperature": row["temperature"],
            }
        )
    _df2 = pd.DataFrame(_targets_ref)
    _df2 = _df2.sort_values(by=["time", "id"])
    _df2 = _df2.set_index("time")
    return _df2


def _preprocess_intensity(df, start_date):
    _df = df.copy()
    _df["start"] = pd.to_datetime(_df["start"])
    _df["end"] = pd.to_datetime(_df["end"])
    _df = _df.sort_values(by=["start"])
    bigger_than_start_date = _df["start"] > start_date
    after_heaters_on = _df["start"] > datetime(2023, 11, 1).date().isoformat()
    _df = _df[bigger_than_start_date & after_heaters_on]
    _df = _df.reset_index(drop=True)
    _intensity_ref = []
    for i, row in _df.iterrows():
        _intensity_ref.append(
            {
                "id": i,
                "time": row["start"],
                "intensity": row["intensity"],
            }
        )
        _intensity_ref.append(
            {
                "id": i,
                "time": row["end"],
                "intensity": row["intensity"],
            }
        )
    _df2 = pd.DataFrame(_intensity_ref)
    _df2 = _df2.sort_values(by=["time", "id"])
    _df2 = _df2.set_index("time")
    return _df2


def _use_common_ax_settings(ax):
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m"))
    ax.xaxis.set_major_locator(mdates.WeekdayLocator())
    ax.figure.autofmt_xdate()
    ax.grid(True)
    ax.legend(loc="lower left")


def _plot_measurements_vs_targets(ax, _t, _c):
    ax.set_title(
        f"Living Room Temperatures since {_t.index.min().strftime('%Y-%m-%d')}"
    )
    ax.plot(_t.index, _t["temperature"], label="measured", color="blue")
    ax.plot(_c.index, _c["temperature"], label="commanded", color="red")
    _use_common_ax_settings(ax)


def _plot_heaters_intensity(ax, _h):
    ax.plot(_h.index, _h["intensity"], label="intensity", color="green")
    ax.yaxis.set_major_locator(mdates.AutoDateLocator())
    ax.set_yticks([0, 1, 2, 3])
    ax.set_yticklabels(["NONE", "LOW", "MEDIUM", "HIGH"])
    _use_common_ax_settings(ax)


def _plot(_t, _c, _h):
    fig, axes = plt.subplots(2, 1)
    _plot_measurements_vs_targets(axes[0], _t, _c)
    _plot_heaters_intensity(axes[1], _h)
    axes[0].set_xlim(axes[1].get_xlim())
    plt.show()


def _plot_all_temperatures(_temperatures, targets, heaters_intensity, start_date):
    _t = _preprocess_temperatures(_temperatures, start_date)
    _c = _preprocess_targets(targets, start_date)
    _h = _preprocess_intensity(heaters_intensity, start_date)
    _plot(_t, _c, _h)
