import enum
import os
from datetime import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

plt.switch_backend("TkAgg")


class Granularity(enum.Enum):
    DAY = "day"
    MONTH = "month"


def on_ax_change(ax):
    """if you zoom one plot, the other will follow"""

    def _on_ax_change(event_ax):
        if event_ax != ax:
            ax.set_xlim(event_ax.get_xlim())

    return _on_ax_change


def _use_common_ax_settings(ax, granularity=Granularity.MONTH):
    if granularity == Granularity.MONTH:
        _g = mdates.MonthLocator()
    else:
        _g = mdates.DayLocator()

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m"))
    ax.xaxis.set_major_locator(_g)
    ax.figure.autofmt_xdate()
    ax.grid(True)
    ax.legend(loc="lower left")


def color_seasons(ax, _t):
    # Extract the minimum and maximum dates from the data
    start_date = _t["time"].min().date()
    end_date = _t["time"].max().date()

    # Define season colors
    season_colors = {
        "Winter": "blue",
        "Spring": "yellow",
        "Summer": "orange",
        "Autumn": "brown",
    }

    # Function to get the season boundaries for a given year
    def get_season_boundaries(year):
        return {
            "Winter": (datetime(year - 1, 12, 21).date(), datetime(year, 3, 20).date()),
            "Spring": (datetime(year, 3, 21).date(), datetime(year, 6, 20).date()),
            "Summer": (datetime(year, 6, 21).date(), datetime(year, 9, 22).date()),
            "Autumn": (datetime(year, 9, 23).date(), datetime(year, 12, 20).date()),
        }

    # Iterate over each year in the date range
    for year in range(start_date.year, end_date.year + 1):
        seasons = get_season_boundaries(year)
        for season, (start, end) in seasons.items():
            # Adjust season boundaries to be within the data range
            span_start = max(start_date, start)
            span_end = min(end_date, end)
            if span_start < span_end:
                ax.axvspan(
                    span_start,
                    span_end,
                    color=season_colors[season],
                    alpha=0.2,
                    label=(
                        season
                        if (span_start == start_date or year == start_date.year)
                        else ""
                    ),
                )

    # Optional: Add legend outside the plot
    # TODO: missing winter in the legend
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(
        by_label.values(), by_label.keys(), loc="upper left", bbox_to_anchor=(1, 1)
    )


def _plot_measurements_vs_targets(ax, _a, visual_granularity):
    start_time = _a["time"].min().strftime("%Y-%m-%d")
    ax.set_title(f"Living Room Temperatures since {start_time}")
    ax.plot(_a["time"], _a["measured"], label="measured", color="blue")
    ax.plot(_a["time"], _a["target"], label="target", color="red")
    _use_common_ax_settings(ax, granularity=visual_granularity)
    color_seasons(ax, _a)


def _plot_heaters_intensity(ax, _a, visual_granularity):
    ax.set_title("Heaters Intensity")
    ax.plot(_a["time"], _a["intensity"], label="intensity", color="green")
    ax.yaxis.set_major_locator(mdates.AutoDateLocator())
    ax.set_yticks([0, 1, 2, 3])
    ax.set_yticklabels(["NONE", "LOW", "MEDIUM", "HIGH"])
    _use_common_ax_settings(ax, granularity=visual_granularity)


def _visualise_temperatures(golden_dir, visual_granularity):
    # read
    _t = pd.read_parquet(os.path.join(golden_dir, "temperatures.parquet"))
    _c = pd.read_parquet(os.path.join(golden_dir, "targets.parquet"))
    _h = pd.read_parquet(os.path.join(golden_dir, "intensity.parquet"))

    # create aggregated view
    _t = _t.rename(columns={"temperature": "measured"})
    _c = _c.rename(columns={"temperature": "target"})
    _a = pd.merge(
        _t,
        _c,
        on="time",
        how="left",
    ).merge(
        _h,
        on="time",
        how="left",
    )

    # plot
    fig, axes = plt.subplots(2, 1)
    _plot_measurements_vs_targets(axes[0], _a, visual_granularity)
    _plot_heaters_intensity(axes[1], _a, visual_granularity)
    axes[1].set_xlim(axes[0].get_xlim())
    axes[0].callbacks.connect("xlim_changed", on_ax_change(axes[1]))
    axes[1].callbacks.connect("xlim_changed", on_ax_change(axes[0]))
    plt.show()
