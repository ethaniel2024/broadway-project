# Analysis Summary

## Dataset scope

- Weekly observations after cleaning: `4,329`
- Distinct shows after cleaning: `144`
- Rows without a show name were removed because they could not support show-level analysis.

## Findings

### 1. Do Tony-flagged shows run longer?

Using the dataset's `TonyNominatedMusical` field as the available award-related signal:

- Tony-flagged shows average `49.9` tracked weeks.
- Non-flagged shows average `24.4` tracked weeks.
- Difference: about `25.5` additional tracked weeks for Tony-flagged shows.

### 2. Do larger theaters have higher gross revenue?

Yes, the relationship is clearly positive in this dataset.

- Weekly correlation between theater seats and weekly gross: `0.64`
- Show-level correlation between average theater size and average weekly gross: `0.62`
- Simple linear trend: roughly `$1,193` in weekly gross for each added seat

### 3. Are Tony-flagged shows in larger theaters?

Yes, Tony-flagged shows tend to appear in larger houses.

- Tony-flagged shows average `1,314.4` seats
- Non-flagged shows average `988.1` seats
- Difference: about `326.3` seats

## Interpretation

The three questions point in the same direction: in this dataset, the Tony-related flag is associated with longer tracked runs, larger theaters, and higher weekly revenue. That does not prove the flag causes those outcomes, but it does suggest that award-related prestige and commercial scale move together in the Broadway market represented here.

## Methodology and workflow

This project analyzes a custom Broadway dataset built from publicly accessible source material and stored in `data/raw/Broadway_Data.csv` in this repository. The data used for the package, report, and dashboard are therefore directly available to the user. Because the dataset is custom assembled rather than downloaded as a ready-made analysis file, the reproducible acquisition workflow is also documented in a companion repository: `https://github.com/jessieaolsen-sys/data-aquistion-code`.

After acquisition, the dataset was cleaned and standardized through the `broadway_insights` package. The cleaning workflow parsed dates and currency values, reconstructed ticket-price, performance, preview, and seat-count fields from concatenated source values, and derived run-window metrics such as run start, run end, weeks tracked, and run length in days. These steps created an analysis-ready dataset that could be reused consistently across the written report, package examples, tests, and Streamlit dashboard.

The analysis focused on three motivating questions: whether Tony-flagged shows tend to run longer, whether larger theaters are associated with higher revenue, and whether Tony-flagged shows tend to appear in larger theaters. To answer these questions, the project used grouped summaries, mean comparisons, correlations, and a simple linear trend estimate between theater size and weekly gross. Because the same cleaned dataset powers both the report and the dashboard, the reported findings and interactive outputs are aligned and reproducible.

## Limitation

The file does not contain an explicit award-winning field. It contains `TonyNominatedMusical`, which may not map perfectly to "Tony award winning." All conclusions should therefore be presented as findings about the dataset's Tony-related flag, not definitive proof about actual winners.
