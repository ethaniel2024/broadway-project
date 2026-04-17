"""Plot helpers for the Broadway analysis dashboard."""

from __future__ import annotations

import pandas as pd

from .analysis import summarize_show_runs


def build_revenue_scatter(df: pd.DataFrame):
    """Create a scatterplot of theater size versus weekly gross revenue."""

    import plotly.express as px

    figure = px.scatter(
        df,
        x="seats_in_theatre",
        y="weekly_gross",
        color="tony_nominated",
        size="avg_ticket_price",
        hover_data=["Show", "theater", "week_ending", "capacity_pct"],
        labels={
            "seats_in_theatre": "Theater seats",
            "weekly_gross": "Weekly gross revenue",
            "tony_nominated": "Tony flagged",
            "avg_ticket_price": "Average ticket price",
        },
        title="Weekly Broadway revenue by theater size",
    )
    figure.update_layout(legend_title_text="Tony flagged")
    return figure


def build_run_length_boxplot(df: pd.DataFrame):
    """Create a show-level comparison of tracked run length by Tony flag."""

    import plotly.express as px

    show_summary = summarize_show_runs(df)
    figure = px.box(
        show_summary,
        x="tony_nominated",
        y="weeks_tracked",
        color="tony_nominated",
        labels={"tony_nominated": "Tony flagged", "weeks_tracked": "Tracked run length (weeks)"},
        title="Tracked run length by Tony flag",
        points="all",
        hover_data=["Show", "theater"],
    )
    figure.update_layout(showlegend=False)
    return figure
