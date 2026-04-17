# Broadway Insights

Broadway Insights is a compact analysis package and dashboard for studying Broadway weekly grosses, tracked run lengths, and theater capacity.

## What this project does

- Cleans malformed source columns in the Broadway CSV.
- Aggregates weekly rows to show-level summaries.
- Computes interpretable comparisons tied to the project research questions.
- Provides a Streamlit dashboard for interactive exploration.

## Core questions

- Do Tony-flagged shows run longer in the tracked dataset?
- Do larger theaters have higher weekly gross revenue?
- Do Tony-flagged shows appear in larger theaters?

## Important limitation

The original file contains a field called `TonyNominatedMusical`. Because the dataset does not include a separate award-winning column, the package treats this field as the available award-related signal and labels it clearly throughout the docs and dashboard.
