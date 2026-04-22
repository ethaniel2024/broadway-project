"""Data loading and cleaning utilities for the Broadway dataset."""

"""This module handles data loading and cleaning for the broadway_insights package. 
load_raw_data reads the bundled (or a user-supplied) Broadway CSV, and clean_broadway_data transforms it into an analysis-ready DataFrame —
renaming columns, parsing currency and date fields, splitting concatenated ticket-price, performance/preview, and seat-count strings back 
into separate numeric columns, and deriving run-window metrics (start, end, weeks tracked, run length in days) per show. A key challenge 
is the _split_seat_counts helper, which recovers seats_sold and seats_in_theatre from a single concatenated digit string by testing every
possible split point and selecting the partition whose inferred capacity percentage best matches the reported value. load_clean_data wraps
both steps into a single convenience call."""

from __future__ import annotations

from importlib.resources import files
from pathlib import Path

import pandas as pd


DEFAULT_DATA_FILE = files("broadway_insights").joinpath("data/Broadway_Data.csv")


def load_raw_data(path: str | Path | None = None) -> pd.DataFrame:
    """Load the raw Broadway CSV.

    Args:
        path: Optional custom CSV path. If omitted, the packaged dataset is used.

    Returns:
        Raw dataframe exactly as stored in the CSV.
    """

    source = Path(path) if path is not None else Path(str(DEFAULT_DATA_FILE))
    return pd.read_csv(source)


def _parse_currency(series: pd.Series) -> pd.Series:
    cleaned = (
        series.astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    return pd.to_numeric(cleaned, errors="coerce")


def _split_ticket_prices(value: object) -> tuple[float | None, float | None]:
    text = str(value).strip()
    if not text:
        return None, None

    parts: list[float] = []
    for piece in text.split("$"):
        piece = piece.replace(",", "").strip()
        if piece:
            try:
                parts.append(float(piece))
            except ValueError:
                continue

    if not parts:
        return None, None
    if len(parts) == 1:
        return parts[0], None
    return parts[0], parts[1]


def _split_perfs_previews(value: object) -> tuple[int, int]:
    text = str(value).strip()
    if not text:
        return 0, 0
    if len(text) == 1:
        return int(text), 0
    return int(text[:-1]), int(text[-1])


def _split_seat_counts(raw_value: object, weekly_capacity_pct: float, performances: int, previews: int) -> tuple[int, int]:
    """Recover seats sold and theatre size from a concatenated field.

    The dataset stores values such as ``9,5081,727`` where the first part is
    seats sold during the week and the second part is theatre capacity.
    We recover the split by choosing the partition that best reproduces the
    reported weekly capacity percentage.
    """

    digits = str(raw_value).replace(",", "").strip()
    if not digits:
        return 0, 0

    total_staged = max(performances + previews, 1)
    best_split: tuple[int, int] | None = None
    best_error = float("inf")

    for index in range(1, len(digits)):
        seats_sold = int(digits[:index])
        seats_in_theatre = int(digits[index:])
        if seats_in_theatre == 0:
            continue
        inferred_pct = seats_sold / (seats_in_theatre * total_staged) * 100
        error = abs(inferred_pct - weekly_capacity_pct)
        if error < best_error:
            best_error = error
            best_split = (seats_sold, seats_in_theatre)

    if best_split is None:
        return 0, 0
    return best_split


def clean_broadway_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the Broadway dataset into analysis-ready columns.

    Args:
        df: Raw dataframe from :func:`load_raw_data`.

    Returns:
        Cleaned dataframe with typed columns and derived run metrics.
    """

    cleaned = df.copy()
    cleaned = cleaned.rename(
        columns={
            "This Week GrossPotential Gross": "weekly_gross",
            "Diff $": "gross_diff",
            "Avg TicketTop Ticket": "avg_ticket_price",
            "Seats SoldSeats in Theatre": "seat_summary",
            "PerfsPreviews": "perfs_previews",
            "% Cap": "capacity_pct",
            "Diff % cap": "capacity_diff_pct",
            "Week Ending": "week_ending",
            "TonyNominatedMusical": "tony_nominated",
            "Theater": "theater",
        }
    )

    cleaned["week_ending"] = pd.to_datetime(cleaned["week_ending"])
    cleaned["gross_diff"] = _parse_currency(cleaned["gross_diff"])
    cleaned = cleaned.dropna(subset=["Show"]).copy()
    cleaned["theater"] = cleaned["theater"].fillna("Unknown Theater")

    ticket_prices = cleaned["avg_ticket_price"].apply(_split_ticket_prices)
    cleaned["avg_ticket_price"] = ticket_prices.str[0]
    cleaned["top_ticket_price"] = ticket_prices.str[1]

    perfs_and_previews = cleaned["perfs_previews"].apply(_split_perfs_previews)
    cleaned["performances"] = perfs_and_previews.str[0]
    cleaned["previews"] = perfs_and_previews.str[1]
    cleaned["total_staged"] = cleaned["performances"] + cleaned["previews"]

    seat_counts = cleaned.apply(
        lambda row: _split_seat_counts(
            raw_value=row["seat_summary"],
            weekly_capacity_pct=row["capacity_pct"],
            performances=row["performances"],
            previews=row["previews"],
        ),
        axis=1,
    )
    cleaned["seats_sold"] = seat_counts.str[0]
    cleaned["seats_in_theatre"] = seat_counts.str[1]

    cleaned["is_large_theater"] = cleaned["seats_in_theatre"] >= cleaned["seats_in_theatre"].median()
    cleaned["run_week_number"] = (
        cleaned.groupby("Show")["week_ending"].rank(method="dense").round().astype("Int64")
    )

    run_windows = cleaned.groupby("Show")["week_ending"].agg(["min", "max", "count"]).rename(
        columns={"min": "run_start", "max": "run_end", "count": "weeks_tracked"}
    )
    cleaned = cleaned.merge(run_windows, on="Show", how="left")
    cleaned["run_length_days"] = (cleaned["run_end"] - cleaned["run_start"]).dt.days

    return cleaned.sort_values(["Show", "week_ending"]).reset_index(drop=True)


def load_clean_data(path: str | Path | None = None) -> pd.DataFrame:
    """Load and clean the Broadway dataset in one step."""

    return clean_broadway_data(load_raw_data(path=path))
