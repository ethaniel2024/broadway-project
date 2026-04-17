from broadway_insights import (
    analyze_award_vs_theater_size,
    analyze_award_weekly_revenue,
    analyze_theater_size_vs_gross,
    load_clean_data,
    summarize_show_runs,
)


def test_show_summary_has_one_row_per_show():
    df = load_clean_data()
    summary = summarize_show_runs(df)
    assert len(summary) == df["Show"].nunique()


def test_analysis_outputs_are_numeric():
    df = load_clean_data()
    revenue = analyze_award_weekly_revenue(df)
    size = analyze_theater_size_vs_gross(df)
    award_size = analyze_award_vs_theater_size(df)

    for result in (revenue, size, award_size):
        assert result
        assert all(isinstance(value, float) for value in result.values())
