# BISL504 final presentation guide

## Eight-minute presentation run of show

| Time | What to say or show |
| --- | --- |
| 0:00–1:00 | State the decision question: how has EV adoption changed across countries, and where should an analyst look more closely? The intended reader is someone comparing market adoption and infrastructure patterns. |
| 1:00–2:00 | Describe the cleaned dataset: 400 country-year rows, 25 countries, 2010–2025. State that the project files do not record a source or licence, so this must be verified before submission. |
| 2:00–3:00 | Explain the preparation decisions in `CleanData.ipynb`: repair header artifacts, convert analytical fields to numeric, trim country names, and remove rows without country or year. The saved cleaned dataset has no missing identifiers; `ev_growth_rate_yoy` has 25 missing values. |
| 3:00–5:00 | Run `streamlit run app.py`. Change the country selection and year range and show that KPIs and charts update together. Switch the trend measure. Open the sales-mix drill-down, hover a point to read its country/year values, then download the filtered rows. |
| 5:00–7:00 | Share two findings supported by the current notebook: the unweighted mean market share across the 25 countries rose from 0.03% in 2010 to 21.67% in 2025; Norway led the 2025 country ranking at 79.96%, followed by Sweden at 53.00% and China at 41.23%. Clarify that these are country-level values, not a global sales-weighted rate. |
| 7:00–8:00 | Cover limitations and next work: confirm source/licence, document how missing growth values are handled, collect peer usability results and actual before/after screenshots, and record the team's AI use and any rejected suggestion. |

## Demo fallback

Start the dashboard before the presentation and keep it open. Capture screenshots of the main views after the first local run so you have a visual fallback; the repository currently has notebook outputs but no dashboard screenshots. Do not attempt a live package installation during the presentation.

## Likely viva questions

- Why use a line chart for change over time and a sorted bar chart for the country comparison?
- What does the country-year grain mean for each point in the scatter plot?
- Why is the charging-station axis logarithmic, and how does that affect interpretation?
- What does the dataset not let you conclude about charging stations and EV adoption?
- What happens to the KPIs when only one country or a shorter year range is selected?
- How would you improve the dashboard for a reader with red-green colour-vision deficiency?
- Which part of the code or design did you build, and how does it work?
- Which AI suggestion did the team reject, and why? Use the team's real disclosure and decisions log; do not invent an answer.

## Session 9 evidence to add before submission

The repository does not contain peer-test observations, accessibility audit results, or before/after screenshots. Run the three-task peer test with the author silent, record answer correctness and time, fix the two largest points of hesitation, and append the real evidence. Add one reasoned AI suggestion rejection only if the team actually made that decision. Keep the presenter's final claims aligned with the recorded results.
