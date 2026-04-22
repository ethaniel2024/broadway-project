"""This Streamlit app serves as the interactive dashboard for the Broadway Insights project.
It loads the cleaned Broadway dataset via the broadway_insights package, caches it for performance, and exposes sidebar filters for Tony-nomination status and theater seat capacity.
The main view displays key metrics (row count, show count, seats-vs-gross correlation) and research-question snapshots (run-length gap, revenue per added seat, theater-size gap)
as headline cards, followed by an interactive Plotly scatterplot of theater size versus weekly gross and a side-by-side layout pairing a run-length boxplot with a top-15 revenue table.
Interpretation notes at the bottom remind users that the Tony flag represents nominations rather than wins and that run length reflects tracked weeks in the dataset, not a show's full Broadway history.
"""

import pandas as pd
import streamlit as st

from broadway_insights.analysis import (
    analyze_award_vs_theater_size,
    analyze_award_weekly_revenue,
    analyze_theater_size_vs_gross,
    summarize_show_runs,
)
from broadway_insights.data import load_clean_data
from broadway_insights.viz import (
    build_revenue_scatter,
    build_run_length_boxplot,
)

st.set_page_config(page_title="Broadway Insights", layout="wide")


@st.cache_data
def get_data() -> pd.DataFrame:
    return load_clean_data()


df = get_data()
show_summary = summarize_show_runs(df)

st.title("Broadway Revenue and Theater Analysis")
st.caption(
    "This dashboard uses the provided Broadway dataset to explore run length, theater size, and revenue patterns."
)

with st.sidebar:
    st.header("Filters")
    selected_tony = st.multiselect(
        "Tony flag",
        options=sorted(df["tony_nominated"].unique().tolist()),
        default=sorted(df["tony_nominated"].unique().tolist()),
    )
    capacity_bounds = st.slider(
        "Theater seats",
        min_value=int(df["seats_in_theatre"].min()),
        max_value=int(df["seats_in_theatre"].max()),
        value=(int(df["seats_in_theatre"].min()), int(df["seats_in_theatre"].max())),
    )

filtered_df = df[
    df["tony_nominated"].isin(selected_tony)
    & df["seats_in_theatre"].between(capacity_bounds[0], capacity_bounds[1])
].copy()

filtered_show_summary = summarize_show_runs(filtered_df)
run_stats = analyze_award_weekly_revenue(filtered_df)
size_stats = analyze_theater_size_vs_gross(filtered_df)
award_size_stats = analyze_award_vs_theater_size(filtered_df)

metric_1, metric_2, metric_3 = st.columns(3)
metric_1.metric("Weekly rows", f"{len(filtered_df):,}")
metric_2.metric("Shows", f"{filtered_show_summary['Show'].nunique():,}")
metric_3.metric("Weekly corr: seats vs gross", f"{size_stats['weekly_correlation']:.2f}")

st.subheader("Research question snapshots")
question_1, question_2, question_3 = st.columns(3)
question_1.metric(
    "Tony-flagged run length gap",
    f"{run_stats['weeks_mean_difference']:.1f} weeks",
    help="Positive values mean Tony-flagged shows run longer in the tracked data.",
)
question_2.metric(
    "Revenue per added seat",
    f"${size_stats['gross_per_added_seat']:.2f}",
    help="Linear trend estimate from weekly observations.",
)
question_3.metric(
    "Tony-flagged theater size gap",
    f"{award_size_stats['avg_seats_difference']:.1f} seats",
    help="Positive values mean Tony-flagged shows tend to appear in larger theaters.",
)

st.subheader("Revenue scatterplot")
st.plotly_chart(build_revenue_scatter(filtered_df), use_container_width=True)

boxplot_col, table_col = st.columns([1, 1])
with boxplot_col:
    st.subheader("Run length comparison")
    st.plotly_chart(build_run_length_boxplot(filtered_df), use_container_width=True)

with table_col:
    st.subheader("Top shows by total tracked revenue")
    st.dataframe(
        filtered_show_summary[["Show", "theater", "weeks_tracked", "avg_seats_in_theatre", "total_revenue"]]
        .head(15)
        .assign(total_revenue=lambda frame: frame["total_revenue"].round(2)),
        use_container_width=True,
    )

st.subheader("Interpretation notes")
st.markdown(
    """
    - The dataset records a `TonyNominatedMusical` flag, not an explicit award-winning field.
    - Run length here means tracked weeks in this dataset, not full Broadway lifetime performance history.
    - The seat and performance fields were reconstructed from concatenated source values during cleaning.
    """
)
