import enum
from datetime import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt

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


def _plot_view(_v, visual_granularity):
    plt.style.use("dark_background")
    fig, ax = plt.subplots(2, 1, sharex=True)

    # plot temperature
    ax[0].plot(_v["time"], _v["temperature_value"], label="measured", color="blue")
    ax[0].scatter(
        _v["temperature_time_raw"],
        _v["temperature_value"],
        label="target",
        color="blue",
        marker="o",
        s=10,
    )

    # plot targets
    ax[0].plot(_v["time"], _v["target_value"], label="measured", color="red")
    ax[0].scatter(
        _v["target_time_raw"],
        _v["target_value"],
        label="target",
        color="red",
        marker="o",
        s=10,
    )
    _use_common_ax_settings(ax[0], granularity=visual_granularity)
    color_seasons(ax[0], _v)

    # plot intensity
    ax[1].plot(_v["time"], _v["intensity_value"], label="intensity", color="green")
    ax[1].scatter(
        _v["intensity_time_raw"],
        _v["intensity_value"],
        label="intensity",
        color="green",
        marker="o",
        s=10,
    )
    _use_common_ax_settings(ax[1], granularity=visual_granularity)
    color_seasons(ax[1], _v)

    plt.show()
