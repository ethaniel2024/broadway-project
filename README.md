# Broadway Insights

`broadway-insights` is an installable Python package and Streamlit dashboard for exploring Broadway revenue patterns, theater size, and run length using the provided Broadway dataset.

## Research questions

- Do Tony-flagged shows run longer in the tracked data?
- Do larger theaters tend to produce higher weekly gross revenue?
- Are Tony-flagged shows placed in larger theaters?

## Live Project Links

- **GitHub Pages Website:** https://ethaniel2024.github.io/broadway-project/
- **Streamlit Dashboard:** https://broadway-project-stat386.streamlit.app/
- **GitHub Repository:** https://github.com/ethaniel2024/broadway-project
- **Data Acquisition Repository:** https://github.com/jessieaolsen-sys/data-aquistion-code

## Project structure

```text
.
├── data/raw/Broadway_Data.csv
├── docs/
├── src/broadway_insights/
├── streamlit_app.py
└── tests/
```

## Installation

```bash
python3 -m pip install -e .
```

For the dashboard dependencies:

```bash
python3 -m pip install -e ".[dashboard]"
```

For development tools:

```bash
python3 -m pip install -e ".[dev,dashboard]"
```

## Quick start

```python
from broadway_insights import load_clean_data, analyze_theater_size_vs_gross

df = load_clean_data()
results = analyze_theater_size_vs_gross(df)
print(results)
```

## Streamlit dashboard

Run the dashboard locally with:

```bash
streamlit run streamlit_app.py
```

## Documentation

The repository includes a GitHub Pages-ready MkDocs site:

- User-facing reference: `docs/reference.md`
- Tutorial: `docs/tutorial.md`
- Deployment workflow: `.github/workflows/docs.yml`

## Data acquisition and reproducibility

The final analysis dataset used in this project is stored in `data/raw/Broadway_Data.csv`. 
Because this is a custom assembled dataset, the reproducible data-acquisition code is documented in a companion repository:

- **Data acquisition code:** https://github.com/jessieaolsen-sys/data-aquistion-code

That companion repository shows how the source data was collected and assembled, while this repository contains the installable package, cleaned workflow, technical report, documentation, and deployed Streamlit dashboard.

## Data note

The source CSV includes concatenated seat and performance fields. The package reconstructs:

- `seats_sold`
- `seats_in_theatre`
- `performances`
- `previews`

The dataset also provides a `TonyNominatedMusical` flag rather than a direct award-winning indicator, so results should be interpreted with that limitation in mind.
