"""Analysis helpers for the Broadway research questions."""

from __future__ import annotations

import math

import numpy as np
import pandas as pd


def _safe_corr(x: pd.Series, y: pd.Series) -> float:
    if x.nunique() < 2 or y.nunique() < 2:
        return float("nan")
    return float(x.corr(y))


def summarize_show_runs(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate the weekly dataset to one row per show."""

    summary = (
        df.groupby("Show", as_index=False)
        .agg(
            theater=("theater", "first"),
            tony_nominated=("tony_nominated", "first"),
            run_start=("run_start", "first"),
            run_end=("run_end", "first"),
            weeks_tracked=("weeks_tracked", "first"),
            run_length_days=("run_length_days", "first"),
            avg_weekly_gross=("weekly_gross", "mean"),
            median_weekly_gross=("weekly_gross", "median"),
            avg_ticket_price=("avg_ticket_price", "mean"),
            avg_capacity_pct=("capacity_pct", "mean"),
            avg_seats_in_theatre=("seats_in_theatre", "mean"),
            total_revenue=("weekly_gross", "sum"),
        )
        .sort_values("total_revenue", ascending=False)
        .reset_index(drop=True)
    )
    return summary


def _two_group_summary(df: pd.DataFrame, value_col: str, group_col: str) -> dict[str, float]:
    grouped = df.groupby(group_col)[value_col]
    means = grouped.mean().to_dict()
    medians = grouped.median().to_dict()
    counts = grouped.size().to_dict()
    diff = means.get(True, math.nan) - means.get(False, math.nan)
    return {
        "mean_false": float(means.get(False, math.nan)),
        "mean_true": float(means.get(True, math.nan)),
        "median_false": float(medians.get(False, math.nan)),
        "median_true": float(medians.get(True, math.nan)),
        "count_false": int(counts.get(False, 0)),
        "count_true": int(counts.get(True, 0)),
        "mean_difference": float(diff),
    }


def analyze_award_weekly_revenue(df: pd.DataFrame) -> dict[str, float]:
    """Compare tracked run length and weekly revenue by Tony flag.

    The source dataset includes ``tony_nominated`` rather than an explicit
    award-winning flag, so this analysis should be read as a comparison between
    Tony-flagged and non-flagged shows in the provided data.
    """

    show_summary = summarize_show_runs(df)
    run_summary = _two_group_summary(show_summary, "weeks_tracked", "tony_nominated")
    revenue_summary = _two_group_summary(show_summary, "avg_weekly_gross", "tony_nominated")
    return {
        "weeks_mean_difference": run_summary["mean_difference"],
        "weeks_mean_tony_false": run_summary["mean_false"],
        "weeks_mean_tony_true": run_summary["mean_true"],
        "revenue_mean_difference": revenue_summary["mean_difference"],
        "revenue_mean_tony_false": revenue_summary["mean_false"],
        "revenue_mean_tony_true": revenue_summary["mean_true"],
    }


def analyze_theater_size_vs_gross(df: pd.DataFrame) -> dict[str, float]:
    """Measure whether larger theaters are associated with higher revenue."""

    weekly_corr = _safe_corr(df["seats_in_theatre"], df["weekly_gross"])
    show_summary = summarize_show_runs(df)
    show_corr = _safe_corr(show_summary["avg_seats_in_theatre"], show_summary["avg_weekly_gross"])

    slope, intercept = np.polyfit(df["seats_in_theatre"], df["weekly_gross"], deg=1)
    return {
        "weekly_correlation": weekly_corr,
        "show_level_correlation": show_corr,
        "gross_per_added_seat": float(slope),
        "intercept": float(intercept),
    }


def analyze_award_vs_theater_size(df: pd.DataFrame) -> dict[str, float]:
    """Compare theater size between Tony-flagged and non-flagged shows."""

    show_summary = summarize_show_runs(df)
    theater_summary = _two_group_summary(show_summary, "avg_seats_in_theatre", "tony_nominated")
    return {
        "avg_seats_difference": theater_summary["mean_difference"],
        "avg_seats_tony_false": theater_summary["mean_false"],
        "avg_seats_tony_true": theater_summary["mean_true"],
    }
