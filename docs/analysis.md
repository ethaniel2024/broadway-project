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

This project builds a custom Broadway dataset by combining publicly accessible Broadway show data into a single analysis-ready file. The workflow began with collecting weekly show-level information on revenue, ticket prices, attendance, theater size, and Tony nomination status. Because several source fields were stored in concatenated form, the cleaning process reconstructed separate variables such as average ticket price, top ticket price, performances, previews, seats sold, and seats in theatre.

After cleaning, the dataset was standardized into consistent column names and data types. Dates were parsed into proper datetime format, currency fields were converted to numeric values, and show-level run metrics such as run start, run end, weeks tracked, and run length in days were derived from the weekly observations. These steps produced a reproducible dataset that could be used for both descriptive analysis and the Streamlit dashboard.

The analysis focused on three motivating questions: whether Tony-flagged shows tend to run longer, whether larger theaters are associated with higher revenue, and whether Tony-flagged shows tend to appear in larger theaters. To answer these questions, the project used grouped summaries, mean comparisons, correlations, and simple linear trend estimates. The same cleaned dataset powers both the written report and the interactive Streamlit app, ensuring that the reported findings and dashboard outputs are based on the same reproducible workflow.

## Limitation

The file does not contain an explicit award-winning field. It contains `TonyNominatedMusical`, which may not map perfectly to "Tony award winning." All conclusions should therefore be presented as findings about the dataset's Tony-related flag, not definitive proof about actual winners.
