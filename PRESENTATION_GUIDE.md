# BISL504 final presentation guide

## Eight-minute presentation run of show

| Time | What to say or show |
| --- | --- |
| 0:00–1:00 | State the decision question: how has EV adoption changed across countries, and where should an analyst look more closely? Name the intended reader. |
| 1:00–2:00 | Describe the data: the supplied file has 1,200 rows; the analysis table has 400 country-year rows, 25 countries and 2010–2025 coverage. The files do not record the publisher or licence. |
| 2:00–3:00 | Explain the preparation decisions in `build_project.py`: sum vehicle sales across the three source records per country-year, retain other fields only when they agree, then recalculate totals, market share and growth. Explicitly flag that no source field explains the three-record grain; ask the instructor to confirm the aggregation. |
| 3:00–5:00 | Run `streamlit run app.py`. Change the country selection and year range and show that KPIs and charts update together. Switch the trend measure. Open the sales-mix drill-down, hover a point to read its country/year values, then download the filtered rows. |
| 5:00–7:00 | Share three findings: the unweighted mean country share rose from 0.03% in 2010 to 21.67% in 2025; Norway led the 2025 sample at 79.96%; and the pooled Spearman rank association between station counts and EV share is 0.88 among the 375 country-years with positive station counts. The last result is descriptive, may reflect country and time differences, and is not causal. |
| 7:00–8:00 | Cover limitations and next work: verify source/licence and source-record grain, collect peer usability results and real before/after screenshots, confirm the aggregation decision, and complete the team's AI disclosure. |

## Demo fallback

Start the dashboard before the presentation and keep it open. The `figs/` folder contains static chart exports for a visual fallback; they cannot demonstrate filters or drill-down. Capture dashboard screenshots after the team runs its peer test. Do not attempt a live package installation during the presentation.

## Likely viva questions

- Why use a line chart for change over time and a sorted bar chart for the country comparison?
- What do the three source records per country-year represent, and why is summing their sales justified?
- What does the country-year grain mean for each point in the scatter plot?
- Why is the charging-station axis logarithmic, and how does that affect interpretation?
- What does the dataset not let you conclude about charging stations and EV adoption?
- What happens to the KPIs when only one country or a shorter year range is selected?
- How would you improve the dashboard for a reader with red-green colour-vision deficiency?
- Which part of the code or design did you build, and how does it work?
- Which AI suggestion did the team reject, and why? Use the team's real disclosure and decisions log; do not invent an answer.

## Semester End Test practice

Rehearse three unplanned changes to the dashboard within twenty minutes: add or change a filter, change the aggregation, and replace a chart type. Run the project from a fresh terminal with relative paths before the exam machine demonstration.

## Session 9 evidence to add before submission

The repository does not contain peer-test observations, accessibility audit results, or before/after screenshots. Run the three-task peer test with the author silent, record answer correctness and time, fix the two largest points of hesitation, and append the real evidence. Add one reasoned AI suggestion rejection only if the team actually made that decision. Keep the presenter's final claims aligned with the recorded results.
