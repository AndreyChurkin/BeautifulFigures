"""
Not a very beautiful price surface.....

A complex dataset is selected: real DK1 day-ahead prices from the ENTSO-E Transparency Platform.
The data is given in the form of "Day × Time × Price", which allows us to visualise it in 3D.

Note that 3D is not always the best solution: data may overlap, and the perspective distortion 
makes it difficult to read z-axis values.
Yet, a well-made 3D plot can create a WOW effect, instantly showing how interesting/complex/beautiful your data is.

....
....

Andrey Churkin https://andreychurkin.ru/

"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg") # force non-interactive Agg backend so that the script never tries to pop up a GUI window
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pandas as pd
from matplotlib.colors import Normalize



# ============================================================
# DATA & VISUALISATION SETTINGS
# ============================================================

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = SCRIPT_DIR.parent.parent / "data"  # ../../data, shared at the example level (not under Python/)
OUTPUT_DIR = SCRIPT_DIR.parent / "output_figures"


""" Select the dataset and the range of dates to visualise """

DATASET = "DK1_GUI_ENERGY_PRICES_202512312300-202612312300.csv"
START_DATE = "2026-01-01"  # inclusive, local CET/CEST calendar date
END_DATE = "2026-07-15"    # inclusive, local CET/CEST calendar date

# DATASET = "DK1_GUI_ENERGY_PRICES_202412312300-202512312300.csv"
# START_DATE = "2025-01-01"  # inclusive, local CET/CEST calendar date
# END_DATE = "2025-12-31"    # inclusive, local CET/CEST calendar date

# DATASET = "DK1_GUI_ENERGY_PRICES_202312312300-202412312300.csv"
# START_DATE = "2024-01-01"  # inclusive, local CET/CEST calendar date
# END_DATE = "2024-12-31"    # inclusive, local CET/CEST calendar date

# DATASET = "DK1_GUI_ENERGY_PRICES_202212312300-202312312300.csv"
# START_DATE = "2023-01-01"  # inclusive, local CET/CEST calendar date
# END_DATE = "2023-12-31"    # inclusive, local CET/CEST calendar date

# Colormap to use:
# TEST_CMAP = "viridis"  # matplotlib's default colormap
# TEST_CMAP = "rainbow"  # oh no...
TEST_CMAP = "gist_rainbow"  # oh no...
# TEST_CMAP = "jet" # oh no...
# TEST_CMAP = "hsv" # oh no...

# Facet colour rule - how each polygon's colour is computed from its 4 corner Z-values:
#   "mean" -> matplotlib's default flat shading (colours each facet by the average of its 4 corners). 
#             A single-cell spike's facet colour is pulled toward its neighbours and never reaches the true max.
#   "max"  -> colours each facet by the maximum of its 4 corners instead.
#             The true data peak's colour actually reaches the colormap's endpoint.
FACET_COLOUR_RULE = "mean"
# FACET_COLOUR_RULE = "max"

# Whether to apply matplotlib's directional-lighting shading on top of the facet colours:
USE_SHADES = False # Off keeps colours matching the colorbar exactly
# USE_SHADES = True


# That's it! No more plotting or colour settings. Let's see what the default plotting will give us.

# ============================================================


def load_price_grid(dataset: str, start_date: str, end_date: str):
    """ Load ENTSO-E day-ahead prices for [START_DATE, END_DATE] as a (time-of-day × day × price) grid.
        The dates are inclusive. Time format is CET/CEST calendar dates as given in the file.
        Returns (day_grid, hour_grid, price_grid, dates, zone). """
    dataset_path = Path(dataset)
    if not dataset_path.is_absolute():
        dataset_path = DATA_DIR / dataset_path
    df = pd.read_csv(dataset_path)
    zone = df["Area"].iloc[0].removeprefix("BZN|")

    # "MTU (CET/CEST)" is "start - end" in local time. 
    # Right around DST transitions ENTSO-E appends an explicit "(CET)"/"(CEST)" suffix 
    # to disambiguate the spring-forward gap and the autumn fall-back doubled hour.
    # Strip it, since only the plain local start time is needed here.
    start_str = (df["MTU (CET/CEST)"].str.split(" - ").str[0]
                 .str.split(" (", regex=False).str[0])
    timestamp = pd.to_datetime(start_str, format="%d/%m/%Y %H:%M:%S")
    price = pd.to_numeric(df["Day-ahead Price (EUR/MWh)"], errors="coerce")

    s = pd.Series(price.values, index=timestamp).dropna()

    start = pd.Timestamp(start_date)
    end = pd.Timestamp(end_date) + pd.Timedelta(days=1)  # make end_date inclusive
    s = s[(s.index >= start) & (s.index < end)]
    if s.empty:
        raise ValueError(f"No data found between {start_date} and {end_date} in {dataset}")

    tmp = pd.DataFrame({
        "day": s.index.normalize(),
        "tod": s.index.hour + s.index.minute / 60,
        "price": s.values,
    })
    # aggfunc="mean" absorbs both the autumn fall-back doubled local hour and
    # any republished ("Sequence 2" etc.) duplicate rows sharing the same MTU.
    grid = tmp.pivot_table(index="day", columns="tod", values="price", aggfunc="mean")

    # Resolution isn't consistent across exports (hourly in older files, 15-minute in newer ones).
    # Infer the step from the data.
    cols = np.sort(grid.columns.values)
    step = np.diff(cols).min() if len(cols) > 1 else 1.0
    grid = grid.reindex(columns=np.arange(0, 24, step)).sort_index()

    # The spring-forward DST date is missing its skipped local hour's cell(s).
    # For this figure we interpolate it so the surface renders without a hole.
    grid = grid.interpolate(axis=1, limit_direction="both")

    dates = pd.to_datetime(grid.index)
    tods = grid.columns.values
    day_index = np.arange(len(dates))
    price_grid = grid.values.T  # shape (n_tod_bins, n_days)
    day_grid, hour_grid = np.meshgrid(day_index, tods)
    return day_grid, hour_grid, price_grid, dates, zone


def plot_price_surface(day_grid, hour_grid, price_grid, dates, zone, out_path, TEST_CMAP, FACET_COLOUR_RULE, USE_SHADES):
    start, end = dates.min(), dates.max()  # actual plotted range, not the requested START_DATE/END_DATE

    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")

    # This norm (built from the real data range) keeps the colorbar honest.
    color_norm = Normalize(vmin=price_grid.min(), vmax=price_grid.max())
    cmap = plt.get_cmap(TEST_CMAP)

    # Facet colour is always computed manually and passed via facecolors (rather than letting
    # plot_surface derive it from cmap+norm), because that's the only way to make USE_SHADES
    # independent of FACET_COLOUR_RULE - matplotlib silently forces shade=False whenever cmap is
    # passed directly to plot_surface.
    if FACET_COLOUR_RULE == "max":
        # Colour each facet by the MAXIMUM of its 4 corner Z-values, instead of matplotlib's default
        # mean-of-corners flat shading, so the true data peak's colour actually reaches the colormap's endpoint.
        face_value = np.maximum.reduce([
            price_grid[:-1, :-1], price_grid[1:, :-1],
            price_grid[:-1, 1:], price_grid[1:, 1:],
        ])
    elif FACET_COLOUR_RULE == "mean":
        # matplotlib's own default flat shading: a single-cell spike's facet colour is pulled
        # toward its neighbours and never reaches the true max.
        face_value = (price_grid[:-1, :-1] + price_grid[1:, :-1]
                      + price_grid[:-1, 1:] + price_grid[1:, 1:]) / 4.0
    else:
        raise ValueError(f"Unknown FACET_COLOUR_RULE: {FACET_COLOUR_RULE!r} (expected 'mean' or 'max')")

    ax.plot_surface(
        day_grid, hour_grid, price_grid,
        facecolors=cmap(color_norm(face_value)),
        shade=USE_SHADES,
        rstride=1, cstride=1,
    )

    # facecolors bypasses plot_surface's automatic scalar mapping, providing no array for a colorbar.
    # Building a standalone mappable carrying the same cmap/norm.
    mappable = cm.ScalarMappable(norm=color_norm, cmap=cmap)
    mappable.set_array([])
    cbar = fig.colorbar(mappable, ax=ax)

    # Two title lines, with two font sizes.
    # Both use fig.suptitle/fig.text (not ax.set_title) to center on the whole figure canvas.
    title_range = f"{start:%Y-%m-%d} to {end:%Y-%m-%d}"
    fig.suptitle(
        f"{zone} day-ahead price \n {title_range}"
    )

    ax.set_xlabel("Month")
    ax.set_ylabel("Hour of day")
    # No z-axis text label: the colorbar already carries the title

    # Month-start ticks spanning the range of dates plotted:
    month_starts = pd.date_range(start.replace(day=1), end, freq="MS")
    month_positions = [(month_start - dates[0]).days for month_start in month_starts]
    ax.set_xticks(month_positions)
    ax.set_xticklabels(
        [month_start.strftime("%b") for month_start in month_starts]
    )

    # Simple fixed hour ticks, evenly spaced every 4 hours
    hour_ticks = [0, 4, 8, 12, 16, 20, 24]
    ax.set_yticks(hour_ticks)
    ax.set_yticklabels([str(h) for h in hour_ticks])

    cbar.set_label("Price, EUR/MWh")

    fig.savefig(out_path.with_suffix(".png"))

    plt.close(fig)
    return out_path


if __name__ == "__main__":
    day_grid, hour_grid, price_grid, dates, zone = load_price_grid(DATASET, START_DATE, END_DATE)

    OUTPUT_DIR.mkdir(exist_ok=True)
    if TEST_CMAP in ["rainbow", "gist_rainbow", "jet", "hsv"] :
        out_path = OUTPUT_DIR / f"oh_no_rainbow_3d_price_surface_{zone}_{dates.min():%Y%m%d}_{dates.max():%Y%m%d}_{FACET_COLOUR_RULE}.png"
    else:
        out_path = OUTPUT_DIR / f"not_a_very_beautiful_3d_price_surface_{zone}_{dates.min():%Y%m%d}_{dates.max():%Y%m%d}_{FACET_COLOUR_RULE}.png"
    plot_price_surface(day_grid, hour_grid, price_grid, dates, zone, out_path, TEST_CMAP, FACET_COLOUR_RULE, USE_SHADES)
    print(f"\nSaved {out_path.stem}.png to {OUTPUT_DIR}")

    imax = np.unravel_index(np.argmax(price_grid), price_grid.shape)
    imin = np.unravel_index(np.argmin(price_grid), price_grid.shape)
    max_date, max_hour = dates[imax[1]], hour_grid[imax]
    min_date, min_hour = dates[imin[1]], hour_grid[imin]

    print("\nprice_grid.max() = ", price_grid.max(), f" at {max_date:%Y-%m-%d} {max_hour:05.2f}h")
    print("price_grid.min() = ", price_grid.min(), f" at {min_date:%Y-%m-%d} {min_hour:05.2f}h")
