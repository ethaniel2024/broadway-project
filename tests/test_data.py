"""Tests to check the package data cleaning functions work correctly"""
from broadway_insights import clean_broadway_data, load_raw_data


def test_clean_broadway_data_creates_expected_columns():
    raw = load_raw_data()
    cleaned = clean_broadway_data(raw)

    expected = {
        "weekly_gross",
        "gross_diff",
        "avg_ticket_price",
        "capacity_pct",
        "week_ending",
        "tony_nominated",
        "theater",
        "performances",
        "previews",
        "total_staged",
        "seats_sold",
        "seats_in_theatre",
        "weeks_tracked",
        "run_length_days",
    }
    assert expected.issubset(cleaned.columns)


def test_seat_split_matches_known_first_row():
    raw = load_raw_data()
    cleaned = clean_broadway_data(raw)
    first_row = cleaned.iloc[0]

    assert first_row["Show"] == "1776"
    assert first_row["seats_sold"] > 0
    assert first_row["seats_in_theatre"] > 0
    inferred_capacity = first_row["seats_sold"] / (
        first_row["seats_in_theatre"] * max(first_row["total_staged"], 1)
    ) * 100
    assert abs(inferred_capacity - first_row["capacity_pct"]) < 0.2
