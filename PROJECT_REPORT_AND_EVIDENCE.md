# Electric Vehicle Adoption Across Countries

## BISL504 Data Visualization Lab project report and evidence map

**Course:** BISL504 Data Visualization Lab, V Semester, Odd Semester 2026–27  
**Group number and members:** Complete from the approved group register  
**Section and presentation date:** Complete from the faculty running order  
**Project domain:** Electric vehicle adoption, vehicle sales, charging infrastructure and transport emissions

## Project summary

This project explores how electric vehicle (EV) market share changes across countries and how the pattern varies by market. The working dashboard lets a reader compare adoption over time, rank countries for a selected year, inspect the relationship between station counts and EV share, and drill into one country’s vehicle sales mix. The figures support descriptive comparison; they do not establish that charging infrastructure causes EV adoption or emissions changes.

The workspace contains a selected-column source table with 1,200 rows and an analysis table with 400 country-year rows. The build script now reproduces the 400-row table and four labelled figures. The interactive dashboard and final presentation are included in the same project folder.

**Important data decision:** every country-year has three source records, but the source file has no field identifying what those three records represent. The existing cleaning notebook sums the three sales values and keeps the other country-year fields once. The non-sales fields agree within each country-year, and the results reconcile, but the meaning of the three records must be checked against the original source before the aggregated totals are treated as market-wide totals.

## Decision question, audience and scope

**Guiding question:** How has EV adoption changed, and how does it vary across countries?

**Intended reader:** an analyst or decision-maker comparing country-level adoption patterns and identifying markets for further investigation.

### Working objectives

1. Describe the country-level EV market-share trend from 2010 through 2025.
2. Compare countries by EV market share in a selected year.
3. Explore how charging-station counts align with EV market share across country-year records.

The vehicle-sales mix and transport-emissions views provide secondary context. The project does not predict future adoption, estimate policy effects, or rank countries by total EV volume.

## Dataset profile and data preparation

| Check | Selected-column source | Analysis-ready table |
| --- | ---: | ---: |
| Rows and columns | 1,200 × 16 | 400 × 16 |
| Grain | Three records per country-year; the source does not label their sub-grain | One row per country-year |
| Coverage | 25 countries, 2010–2025 | Complete 25 × 16 country-year panel |
| Exact duplicate rows | 0 | 0 |
| Duplicate country-year keys | 800 repeated-key rows across 400 groups of three | 0 |
| Missing country or year | 0 | 0 |
| Other missing values | 0 in the supplied source | 25 in `ev_growth_rate_yoy`; one baseline year per country |
| Negative sales or station counts | 0 | 0 |
| EV market-share range | — | 0.00% to 82.31% |

The 16 fields are one country label, one year field, and 14 numeric measures/indicators. They include sales by vehicle type, market share, charging stations, vehicle range, energy prices, transport emissions, subsidies, regulation score, year-over-year growth and an EV-dominance flag.

| Field | Type in analysis table | Distinct values | Missing |
| --- | --- | ---: | ---: |
| `country` | text | 25 | 0 |
| `year` | integer | 16 | 0 |
| `ev_sales` | integer | 381 | 0 |
| `petrol_car_sales` | integer | 400 | 0 |
| `diesel_car_sales` | integer | 400 | 0 |
| `total_vehicle_sales` | integer | 400 | 0 |
| `ev_market_share` | decimal | 255 | 0 |
| `charging_stations` | integer | 380 | 0 |
| `avg_ev_range_km` | integer | 239 | 0 |
| `fuel_price_usd_per_liter` | decimal | 237 | 0 |
| `electricity_price_usd_per_kwh` | decimal | 197 | 0 |
| `co2_emissions_transport_mt` | decimal | 351 | 0 |
| `ev_subsidy_usd` | integer | 294 | 0 |
| `emission_regulation_score` | decimal | 315 | 0 |
| `ev_growth_rate_yoy` | decimal | 373 | 25 |
| `is_ev_dominant` | integer indicator | 2 | 0 |

### Preparation decisions

- Clean the column names and trim country labels; parse the year and analysis fields as numeric.
- Remove rows with a missing country or year. The supplied source has none, so no rows were removed for these identifiers.
- Aggregate the three records within each country-year by summing EV, petrol and diesel sales.
- Keep charging stations, range, prices, emissions, subsidies and regulation score once per key only after confirming each is identical across the three source records. The build script stops if a conflict appears.
- Recalculate total vehicle sales, EV market share, year-over-year growth and the 50% EV-dominance indicator after aggregation.
- Retain the 25 missing growth values because the first observed year for each country has no prior year for a growth calculation.
- Flag, but do not delete, candidate outliers using the 1.5 × IQR rule: 50 EV market-share values, 39 station counts, 32 emissions values and 46 EV-sales values. The distribution is skewed, so an IQR flag alone is not evidence of an error.

The source name does not document its publisher, URL or licence. Add the original source and reuse terms here before submission. Do not cite the local filename as a source.

### Session 2 tool-trial record to complete

The project files show Python notebooks and the current Streamlit/Plotly dashboard, but do not show three trials of the same chart, elapsed times, or the AI comparison verification. The manual requires measured evidence, so enter the actual trial results rather than inferred ratings.

| Candidate tool | Same market-share chart produced (file/link) | Fit to data type | Interactivity | Audience | Time to first chart (seconds) | Reproducibility | Available at SET | AI claim checked and result |
| --- | --- | --- | --- | --- | ---: | --- | --- | --- |
| Matplotlib |  |  |  |  |  |  |  |  |
| Plotly / Streamlit |  |  |  |  |  |  |  |  |
| Tableau Public or another candidate actually trialled |  |  |  |  |  |  |  |  |

The current tool choice is Python with pandas, Plotly and Streamlit because the project already uses pandas and the dashboard needs linked filters, hover details and a drill-down. This is the design rationale for the current implementation; it is not a substitute for the hands-on comparison or measured times.

## Question-to-chart plan and findings

| Intent | Question | Chart and reason | Result in the supplied data |
| --- | --- | --- | --- |
| Trend over time | How did EV market share change across the country sample? | Line chart of the unweighted mean by year; line slope shows trend while each country-year remains the unit of analysis. | Mean country-level share rose from 0.03% in 2010 to 21.67% in 2025. This is not a sales-weighted global share. |
| Comparison | Which countries had the highest EV share in 2025? | Sorted horizontal bar chart; bar length makes the ranking direct to compare. | Norway led at 79.96%, followed by Sweden at 53.00% and China at 41.23%. |
| Relationship | How do charging-station counts align with EV share? | Scatter plot; the station-count axis is logarithmic because counts span several orders of magnitude. Hover details identify country and year. | Spearman rank correlation is 0.88 for the 375 country-year rows with positive station counts. This pooled association may reflect country and time differences and is not causal evidence. Zero station counts are omitted from the log-scale scatter. |

Figure exports: [market-share trend](figs/ev_market_share_trend.png), [2025 country ranking](figs/ev_market_share_ranking.png), [stations and EV share](figs/charging_stations_vs_ev_share.png), and [transport-emissions trend](figs/transport_emissions_trend.png).

The dashboard also shows transport-emissions trends and a selected-country sales-mix drill-down. In the supplied table, the unweighted mean of transport emissions peaks at 204.8 Mt in 2018 and is 184.7 Mt in 2025. Country means are unweighted. Transport emissions cover more than passenger cars and cannot be attributed to EV adoption alone.

## Dashboard proposal and wireframe

The current Streamlit dashboard follows this reading order:

```text
┌──────────────────── Filter rail ────────────────────┐
│ Country selection · Year range · Trend measure       │
└─────────────────────────────────────────────────────┘
┌──────────────────── KPI strip ──────────────────────┐
│ Mean EV share · EV sales in period · Countries       │
└─────────────────────────────────────────────────────┘
┌──────────────────────────┬──────────────────────────┐
│ EV share / sales trend   │ Country ranking          │
├──────────────────────────┼──────────────────────────┤
│ Stations vs EV share     │ Transport emissions      │
└──────────────────────────┴──────────────────────────┘
┌──────────────── Country sales-mix drill-down ────────┐
│ Vehicle-type bars · hover details · filtered CSV     │
└─────────────────────────────────────────────────────┘
```

### Reconstructed phase timeline

This timeline follows the supplied session manuals; compare it with the group’s approved proposal and add the original decisions log if available.

| Phase | Planned work | Project output |
| --- | --- | --- |
| Session 5 | Clean and profile the selected source data | `build_project.py` and the analysis-ready CSV |
| Session 6 | Build and explain one core chart per guiding question | Four finding-titled chart exports; group walkthrough record still needed |
| Session 7 | Refine labels, annotation, theme and reproducibility; freeze | One-command chart/data rebuild; official freeze record still needed |
| Session 8 | Create the interactive dashboard | `app.py` with shared filters and exploration controls |
| Session 9 | Audit accessibility, peer-test and iterate | Task cards and log template supplied; team must run and record the test |
| Session 10 | Present, demo, answer viva and submit report | Presentation, guide and this report; group review/signoff still needed |
| SET | Demonstrate modifications on the examination machine | Rehearse three live changes within twenty minutes |

One filtered data frame drives all KPIs and views. Readers can filter countries and years, toggle the trend measure, hover for detail, drill into one country and download the filtered rows. The dashboard uses a blue/orange/green colour-blind-safe palette, labels units, uses a log-scale note, and adds a plain-language chart summary below every view.

## Reproducibility and files

From the project directory:

```powershell
python -m pip install -r requirements.txt
python build_project.py
streamlit run app.py
python generate_presentation.py
```

`build_project.py` reads the selected-column CSV by relative path, rebuilds the cleaned dataset, validates its key totals and ranges, prints the missingness/outlier checks, and writes four finding-titled PNGs to `figs/`. `app.py` reads the cleaned CSV beside itself. Run the dashboard on the lab or examination machine before the presentation; package installation during the demo is not a safe fallback.

### Current project files

- `ev_vs_petrol_dataset_v3-selected-columns.csv` — supplied 1,200-row selected-column source file; provenance still needs to be added.
- `build_project.py` — repeatable aggregation, validation and chart export.
- `ev_vs_petrol_dataset_cleaned.csv` — 400-row country-year analysis table.
- `figs/` — four labelled static chart exports for fallback and report use.
- `CleanData.ipynb`, `Graph.ipynb` — existing exploratory/cleaning notebooks.
- `app.py`, `requirements.txt`, `.streamlit/config.toml` — interactive dashboard and runtime setup.
- `generate_presentation.py`, `presentation_base.pptx` — reproducible slide content builder and Office-compatible blank base.
- `BISL504_Final_Project_Presentation.pptx`, `PRESENTATION_GUIDE.md` — final presentation and rehearsal guide.

## Accessibility and Week 9 iteration record

The dashboard uses Okabe–Ito blue, orange and green; avoids using red-versus-green alone; uses labelled axes and restrained gridlines; and supplies one-sentence text summaries beside each chart. Confirm the smallest text on the actual projector and run a contrast/colour-vision check before claiming the accessibility audit is complete.

The repository did not contain a pre-refinement dashboard, peer-test notes, or usability screenshots. Do not fabricate a before/after comparison. Use these task cards with a peer who has not seen the dashboard; the author stays silent and records the answer, correctness, and time.

| Peer task | Correct answer / observation | Correct? | Time | Hesitation and change made |
| --- | --- | --- | --- | --- |
| Among the selected countries, which has the highest EV share in 2025? |  |  |  |  |
| Did the selected countries’ mean EV share rise or fall over the selected years? |  |  |  |  |
| For one selected country, what is the vehicle-sales mix in the last year shown? |  |  |  |  |

| Finding and source | Change made | Before / after evidence |
| --- | --- | --- |
| Complete after the accessibility audit or peer test | Record the actual change | Add actual screenshots |
| Complete after a second actual finding | Record the actual change | Add actual screenshots |
| Record a real AI suggestion the team rejected and the reason; no rejection is documented in the files reviewed so far | Do not invent a disagreement | Link the relevant decision evidence |

## Week 1–10 requirements and evidence status

| Week | Manual deliverable / requirement | Status in the project folder |
| --- | --- | --- |
| 1 | Group formation and domain note | The EV-adoption domain is clear from the data and charts. Group number, member names and the original domain note are not present. |
| 2 | Three hands-on tool trials, six-criterion comparison, verification notes and reasoned tool choice | Python notebooks and a Streamlit/Plotly dashboard are present. The identical-chart trial artifacts, measured time-to-first-chart and AI verification/disagreement notes are not present. The current dashboard stack fits the interactivity requirement; this is not a substitute for trial evidence. |
| 3 | Dataset source/licence, profile, duplicates, candidate outliers and two or three answerable questions | Profile and candidate outliers are documented above. Original source/licence is missing; the approved dataset register and question review are not present. |
| 4 | Approved proposal, question-to-chart mapping, paper wireframe, timeline and peer/AI decisions log | A working proposal and wireframe are reconstructed above. The approved proposal, paper wireframe, group timeline and signed review/decisions log are not present. |
| 5 | Session 5 manual and data-preparation assessment | Session 5 manual was not among the supplied files. The cleaning decisions are documented from `CleanData.ipynb` and checked by `build_project.py`; confirm the exact Session 5 rubric with the course manual. |
| 6 | One correct chart per guiding question, labelled findings and oral walkthrough | Four labelled charts are generated by one script and the dashboard maps to the three guiding questions. The student-by-student oral walkthrough record is not present. |
| 7 | Refinement, annotation, shared theme, reproducibility and freeze | The build script uses relative paths, a consistent theme, annotations, and exports to `figs/`. The official freeze record and student walkthrough evidence are not present. |
| 8 | End-to-end interactive dashboard | Implemented: shared filters, KPI strip, tooltips, measure toggle, country drill-down and filtered-data download. Demonstrate the filter end-to-end during the presentation. |
| 9 | Accessibility audit, peer usability test, before/after evidence and iteration log | Accessible palette and visible chart summaries are implemented. Peer results, contrast/simulator evidence, a genuine before screenshot and completed iteration log remain to be collected. |
| 10 | Timed presentation, live demo, viva, report and AI disclosure log | Presentation and guide are included. Fill in the group details, source/licence, peer-test evidence and the actual team review of the AI disclosure before submission. The live presentation and viva must be unaided. |

## Appendix A — AI disclosure log

AI assistance was used in this project workspace on 29 October 2026 to review the supplied lab manuals and project files; draft the Streamlit dashboard and reproducible build script; calculate and summarize the supplied CSV; and prepare the presentation, report structure and viva guide. Numerical claims were checked against the supplied CSV and the rebuilt analysis table. The project team must review the code, design, data aggregation assumption and claims, and add member names and review date before submission.

**Team members who reviewed the AI-assisted work:** Complete with names and date.  
**Actual suggestion rejected by the team and reason:** No team disagreement is documented in the supplied project materials. Add a real example if applicable; do not create one to fill the row.

## Appendix B — Code and workbook reference

The source code and data are included with this report in the project folder: `build_project.py`, `app.py`, `CleanData.ipynb`, `Graph.ipynb`, `ev_vs_petrol_dataset_v3-selected-columns.csv` and `ev_vs_petrol_dataset_cleaned.csv`. Add the approved repository or shared-drive URL if the instructor requires a link.
