"""Public package interface for broadway_insights."""

"""This is the __init__.py for the broadway_insights package. It re-exports the public API from three internal modules —
data (loading and cleaning), analysis (aggregation and research-question comparisons), and viz (Plotly charts) — 
and declares them in __all__ so that from broadway_insights import * exposes exactly the nine supported functions."""

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
