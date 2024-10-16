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
    start_date = _t.index.min().date()
    end_date = _t.index.max().date()

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


def _plot_measurements_vs_targets(ax, _t, _c, visual_granularity):
    ax.set_title(
        f"Living Room Temperatures since {_t.index.min().strftime('%Y-%m-%d')}"
    )
    ax.plot(_t.index, _t["temperature"], label="measured", color="blue")
    ax.plot(_c.index, _c["temperature"], label="target", color="red")
    _use_common_ax_settings(ax, granularity=visual_granularity)
    color_seasons(ax, _t)


def _plot_heaters_intensity(ax, _h, visual_granularity):
    ax.set_title("Heaters Intensity")
    ax.plot(_h.index, _h["intensity"], label="intensity", color="green")
    ax.yaxis.set_major_locator(mdates.AutoDateLocator())
    ax.set_yticks([0, 1, 2, 3])
    ax.set_yticklabels(["NONE", "LOW", "MEDIUM", "HIGH"])
    _use_common_ax_settings(ax, granularity=visual_granularity)


def plot_aggregates(golden_dir, visual_granularity):
    # read
    _t = pd.read_parquet(os.path.join(golden_dir, "temperatures.parquet"))
    _c = pd.read_parquet(os.path.join(golden_dir, "targets.parquet"))
    _h = pd.read_parquet(os.path.join(golden_dir, "intensity.parquet"))

    # plot
    fig, axes = plt.subplots(2, 1)
    _plot_measurements_vs_targets(axes[0], _t, _c, visual_granularity)
    _plot_heaters_intensity(axes[1], _h, visual_granularity)
    axes[1].set_xlim(axes[0].get_xlim())
    plt.show()
