# Tutorial

## Install the package

```bash
python3 -m pip install -e .
```

To run the Streamlit dashboard, install the dashboard extras as well:

```bash
python3 -m pip install -e ".[dashboard]"
```

## Load the cleaned data

```python
from broadway_insights import load_clean_data

df = load_clean_data()
df.head()
```

## Answer the research questions

```python
from broadway_insights import (
    analyze_award_vs_theater_size,
    analyze_award_weekly_revenue,
    analyze_theater_size_vs_gross,
)

df = load_clean_data()

print(analyze_award_weekly_revenue(df))
print(analyze_theater_size_vs_gross(df))
print(analyze_award_vs_theater_size(df))
```

## Build a chart in Python

```python
from broadway_insights import build_revenue_scatter, load_clean_data

df = load_clean_data()
fig = build_revenue_scatter(df)
fig.show()
```

## Run the Streamlit app

```bash
streamlit run streamlit_app.py
```

## What to look for

- Check whether the Tony-flagged group shows a longer average tracked run.
- Use the scatterplot to inspect how theater capacity and revenue move together.
- Compare average theater size between Tony-flagged and non-flagged shows.
