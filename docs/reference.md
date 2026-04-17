# Function Reference

## `load_raw_data(path=None)`

Purpose: Load the raw Broadway CSV.

Args:
- `path`: Optional path to a CSV file. If omitted, the packaged dataset is used.

Returns:
- `pandas.DataFrame`: The original raw dataset.

Example:

```python
from broadway_insights import load_raw_data

raw_df = load_raw_data()
```

## `clean_broadway_data(df)`

Purpose: Clean malformed fields and derive analysis-ready columns such as seat counts and run metrics.

Args:
- `df`: Raw `pandas.DataFrame` loaded from the Broadway CSV.

Returns:
- `pandas.DataFrame`: Cleaned weekly dataset.

Example:

```python
from broadway_insights import clean_broadway_data, load_raw_data

clean_df = clean_broadway_data(load_raw_data())
```

## `load_clean_data(path=None)`

Purpose: Load and clean the Broadway data in one step.

Args:
- `path`: Optional custom CSV path.

Returns:
- `pandas.DataFrame`: Cleaned weekly dataset.

Example:

```python
from broadway_insights import load_clean_data

df = load_clean_data()
```

## `summarize_show_runs(df)`

Purpose: Aggregate weekly records to one row per show.

Args:
- `df`: Cleaned weekly Broadway dataframe.

Returns:
- `pandas.DataFrame`: Show-level summary with run window, revenue, ticket, and theater metrics.

Example:

```python
from broadway_insights import load_clean_data, summarize_show_runs

summary = summarize_show_runs(load_clean_data())
```

## `analyze_award_weekly_revenue(df)`

Purpose: Compare tracked run length and average weekly revenue between Tony-flagged and non-flagged shows.

Args:
- `df`: Cleaned weekly Broadway dataframe.

Returns:
- `dict[str, float]`: Summary statistics for run length and revenue differences.

Example:

```python
from broadway_insights import analyze_award_weekly_revenue, load_clean_data

results = analyze_award_weekly_revenue(load_clean_data())
```

## `analyze_theater_size_vs_gross(df)`

Purpose: Estimate the relationship between theater size and weekly gross revenue.

Args:
- `df`: Cleaned weekly Broadway dataframe.

Returns:
- `dict[str, float]`: Correlations and a simple linear trend estimate.

Example:

```python
from broadway_insights import analyze_theater_size_vs_gross, load_clean_data

results = analyze_theater_size_vs_gross(load_clean_data())
```

## `analyze_award_vs_theater_size(df)`

Purpose: Compare average theater size for Tony-flagged and non-flagged shows.

Args:
- `df`: Cleaned weekly Broadway dataframe.

Returns:
- `dict[str, float]`: Group averages and the difference in average theater size.

Example:

```python
from broadway_insights import analyze_award_vs_theater_size, load_clean_data

results = analyze_award_vs_theater_size(load_clean_data())
```

## `build_revenue_scatter(df)`

Purpose: Create an interactive scatterplot of theater size versus weekly gross revenue.

Args:
- `df`: Cleaned weekly Broadway dataframe.

Returns:
- `plotly.graph_objects.Figure`: Interactive scatterplot.

Example:

```python
from broadway_insights import build_revenue_scatter, load_clean_data

fig = build_revenue_scatter(load_clean_data())
```

## `build_run_length_boxplot(df)`

Purpose: Visualize tracked run-length differences between Tony-flagged and non-flagged shows.

Args:
- `df`: Cleaned weekly Broadway dataframe.

Returns:
- `plotly.graph_objects.Figure`: Interactive boxplot.

Example:

```python
from broadway_insights import build_run_length_boxplot, load_clean_data

fig = build_run_length_boxplot(load_clean_data())
```
