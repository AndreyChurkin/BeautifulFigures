"""
This example demonstrates how to create beautiful visualisations in 3D.

A complex dataset is selected: real DK1 day-ahead prices from the ENTSO-E Transparency Platform.
The data is given in the form of "Day × Time × Price", which allows us to visualise it in 3D.

Note that 3D is not always the best solution: data may overlap, and the perspective distortion 
makes it difficult to read z-axis values.
Yet, a well-made 3D plot can create a WOW effect, instantly showing how interesting/complex/beautiful your data is.
In this case, 3D is used to create a dramatic visualisation of the difference between calm prices and peaks.

Multiple plotting parameters are fine-tuned to achieve this and produce a clean, publication-ready figure:
- to be added....
-
-

The figure is saved in PDF and SVG formats (vector-based graphics), 
which will allow us to use it in a manuscript without loss of quality.

Andrey Churkin https://andreychurkin.ru/

"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg") # force non-interactive Agg backend so that the script never tries to pop up a GUI window
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap, Normalize, PowerNorm, to_rgb, to_rgba

matplotlib.rcParams["font.family"] = ["Courier New", "monospace"]



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


# Font sizes (tuned independently)
TITLE_FONTSIZE = 20
SUBTITLE_FONTSIZE = 13  # line under the title
AXIS_LABEL_FONTSIZE = 13
TICK_LABEL_FONTSIZE = 11

# Color scale: 
#   Use USE_NONLINEAR_NORM = False for a plain linear scale
#   Use USE_NONLINEAR_NORM = True for a PowerNorm gamma-compresses nonlinear color mapping 
USE_NONLINEAR_NORM = False
GAMMA = 0.6  # <1 boosts contrast in the low/mid range, >1 boosts the high end, 1 == linear

# Colour settings for the dark background:
#   Dark teal radial-gradient background
#   Light ink and gridlines to read on it
BG_GRADIENT_CENTER = "#12302f"
BG_GRADIENT_EDGE = "#071414"
PRIMARY_INK = "#f2f2f0"
GRIDLINE = "#2c4a48"
LOW_PRICE_COLOR = "#2d0b4e"  # deep purple plateau for calm prices
# Inspired by the Purple and Orange Sunset palette https://www.color-hex.com/color-palette/84862
CUSTOM_PALETTE = ["#a11477", "#c1246b", "#e13661", "#fd4c55", "#ff6f4b"]

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

    # "MTU (CET/CEST)" is "start - end" in local wall-clock time. Right around
    # DST transitions ENTSO-E appends an explicit "(CET)"/"(CEST)" suffix to
    # disambiguate the spring-forward gap and the autumn fall-back doubled
    # hour - strip it, since only the plain local start time is needed here.
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

    # Resolution isn't consistent across exports (hourly in older files,
    # 15-minute in newer ones) - infer the step from the data instead of
    # hardcoding one.
    cols = np.sort(grid.columns.values)
    step = np.diff(cols).min() if len(cols) > 1 else 1.0
    grid = grid.reindex(columns=np.arange(0, 24, step)).sort_index()
    # The spring-forward DST date is missing its skipped local hour's cell(s).
    # For this single decorative figure we interpolate it so the surface
    # renders without a hole - a display choice, not for data-integrity CSVs.
    grid = grid.interpolate(axis=1, limit_direction="both")

    dates = pd.to_datetime(grid.index)
    tods = grid.columns.values
    day_index = np.arange(len(dates))
    price_grid = grid.values.T  # shape (n_tod_bins, n_days)
    day_grid, hour_grid = np.meshgrid(day_index, tods)
    return day_grid, hour_grid, price_grid, dates, zone


def build_price_cmap(low_price_fraction: float = 0.1) -> LinearSegmentedColormap:
    """ Low-price plateau with LOW_PRICE_COLOR defined by low_price_fraction, 
        then a smooth ramp into CUSTOM_PALETTE for price spikes. """
    positions = np.linspace(low_price_fraction, 1.0, len(CUSTOM_PALETTE) + 1)[1:]
    stops = [(0.0, LOW_PRICE_COLOR), (low_price_fraction, LOW_PRICE_COLOR)]
    stops += list(zip(positions, CUSTOM_PALETTE))
    return LinearSegmentedColormap.from_list("price", stops)


def build_radial_gradient(width: int, height: int, center_color: str, edge_color: str) -> np.ndarray:
    """ RGB image: radial gradient from center_color (center) to edge_color (corners). """
    center_rgb = np.array(to_rgb(center_color))
    edge_rgb = np.array(to_rgb(edge_color))
    y, x = np.mgrid[0:height, 0:width]
    cx, cy = (width - 1) / 2, (height - 1) / 2
    dist = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
    dist = np.clip(dist / dist.max(), 0.0, 1.0)[..., None]
    return center_rgb * (1 - dist) + edge_rgb * dist


def plot_price_surface(day_grid, hour_grid, price_grid, dates, zone, out_path):
    start, end = dates.min(), dates.max()  # actual plotted range, not the requested START_DATE/END_DATE

    fig = plt.figure(figsize=(8, 6))
    fig.patch.set_facecolor(BG_GRADIENT_EDGE)

    # Radial gradient background. Drawn behind the 3D plot.
    bg_ax = fig.add_axes((0, 0, 1, 1), zorder=-10)
    gradient = build_radial_gradient(400, 300, BG_GRADIENT_CENTER, BG_GRADIENT_EDGE)
    bg_ax.imshow(gradient, extent=(0, 1, 0, 1), aspect="auto", origin="lower")
    bg_ax.axis("off")

    ax = fig.add_subplot(111, projection="3d", facecolor="none")
    # fig.add_subplot(111, ...) claims matplotlib's default subplot rectangle, reserving generous margins.
    # fig.tight_layout() below can't shrink them for a 3D axes. So we claim most of the figure explicitly.
    # Then, we can zoom the 3D box itself to fill more of that rectangle.
    ax.set_box_aspect(None, zoom=1.1)

    # plot_surface colors each face by the mean of its 4 corner Z-values (flat shading), not by vertex height.
    # So, a single-cell spike's face color is pulled toward its neighbors and never reaches the true max.
    # This norm (built from the real data range) keeps the colorbar honest.
    if USE_NONLINEAR_NORM:
        color_norm = PowerNorm(gamma=GAMMA, vmin=price_grid.min(), vmax=price_grid.max())
    else:
        color_norm = Normalize(vmin=price_grid.min(), vmax=price_grid.max())

    surf = ax.plot_surface(
        day_grid, hour_grid, price_grid,
        cmap=build_price_cmap(),
        linewidth=0,
        antialiased=True,
        rstride=1, cstride=1,
        norm=color_norm,
    )

    # Two title lines, with two font sizes.
    # Both use fig.suptitle/fig.text (not ax.set_title) to center on the whole figure canvas.
    title_range = f"{start:%Y-%m-%d} to {end:%Y-%m-%d}"
    fig.suptitle(
        f"{zone} day-ahead price",
        color=PRIMARY_INK, fontsize=TITLE_FONTSIZE, fontweight="bold", y=0.96,
    )
    fig.text(
        0.5, 0.88, title_range,
        color=PRIMARY_INK, fontsize=SUBTITLE_FONTSIZE, fontweight="bold", ha="center",
    )
    ax.set_xlabel("Month", color=PRIMARY_INK, fontsize=AXIS_LABEL_FONTSIZE, labelpad=15)
    ax.set_ylabel("Hour of day", color=PRIMARY_INK, fontsize=AXIS_LABEL_FONTSIZE, labelpad=6)
    # No z-axis text label: the colorbar already carries the title.

    # Month-start ticks spanning whatever range was actually plotted.
    month_starts = pd.date_range(start.replace(day=1), end, freq="MS")
    month_positions = [(month_start - dates[0]).days for month_start in month_starts]
    ax.set_xticks(month_positions)
    ax.set_xticklabels(
        [month_start.strftime("%b") for month_start in month_starts],
        color=PRIMARY_INK, rotation=45, ha="right",
    )

    # Simple fixed hour ticks, evenly spaced every 4 hours
    hour_ticks = [0, 4, 8, 12, 16, 20, 24]
    ax.set_yticks(hour_ticks)
    ax.set_yticklabels([str(h) for h in hour_ticks], color=PRIMARY_INK)

    ax.tick_params(colors=PRIMARY_INK, labelsize=TICK_LABEL_FONTSIZE)
    grid_rgba = to_rgba(GRIDLINE, alpha=0.35)
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.pane.set_facecolor((0, 0, 0, 0))  # transparent, gradient shows through
        axis.pane.set_edgecolor(GRIDLINE)
        axis._axinfo["grid"].update(color=grid_rgba, linewidth=0.5)
    ax.grid(True)

    ax.view_init(elev=30, azim=-60)

    cbar = fig.colorbar(surf, ax=ax, shrink=0.6, pad=0.12)  # pad clears the axis on the right
    cbar.set_label("Price, EUR/MWh", color=PRIMARY_INK, fontsize=AXIS_LABEL_FONTSIZE, labelpad=15)
    cbar.ax.yaxis.set_tick_params(color=PRIMARY_INK, labelsize=TICK_LABEL_FONTSIZE)
    plt.setp(cbar.ax.get_yticklabels(), color=PRIMARY_INK)

    # no fig.tight_layout() - it doesn't work with 3D axes

    for ext in ("png", "pdf", "svg"):
        fig.savefig(out_path.with_suffix(f".{ext}"), dpi=300, facecolor=fig.get_facecolor())
    plt.close(fig)
    return out_path


if __name__ == "__main__":
    day_grid, hour_grid, price_grid, dates, zone = load_price_grid(DATASET, START_DATE, END_DATE)

    OUTPUT_DIR.mkdir(exist_ok=True)
    out_path = OUTPUT_DIR / f"beautiful_3d_price_surface_{zone}_{dates.min():%Y%m%d}_{dates.max():%Y%m%d}.png"
    plot_price_surface(day_grid, hour_grid, price_grid, dates, zone, out_path)
    print(f"Wrote {out_path.stem}.png/.pdf/.svg to {OUTPUT_DIR}")

    imax = np.unravel_index(np.argmax(price_grid), price_grid.shape)
    imin = np.unravel_index(np.argmin(price_grid), price_grid.shape)
    max_date, max_hour = dates[imax[1]], hour_grid[imax]
    min_date, min_hour = dates[imin[1]], hour_grid[imin]

    print("\nprice_grid.max() = ", price_grid.max(), f" at {max_date:%Y-%m-%d} {max_hour:05.2f}h")
    print("price_grid.min() = ", price_grid.min(), f" at {min_date:%Y-%m-%d} {min_hour:05.2f}h")
