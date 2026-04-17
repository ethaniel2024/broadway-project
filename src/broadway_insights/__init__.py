"""Public package interface for broadway_insights."""

from .analysis import (
    analyze_award_vs_theater_size,
    analyze_award_weekly_revenue,
    analyze_theater_size_vs_gross,
    summarize_show_runs,
)
from .data import clean_broadway_data, load_clean_data, load_raw_data
from .viz import build_revenue_scatter, build_run_length_boxplot

__all__ = [
    "analyze_award_vs_theater_size",
    "analyze_award_weekly_revenue",
    "analyze_theater_size_vs_gross",
    "build_revenue_scatter",
    "build_run_length_boxplot",
    "clean_broadway_data",
    "load_clean_data",
    "load_raw_data",
    "summarize_show_runs",
]
