"""Interactive EV adoption dashboard for the BISL504 Data Visualization Lab."""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(page_title="Electric vehicle adoption", page_icon="⚡", layout="wide")

DATA_PATH = Path(__file__).with_name("ev_vs_petrol_dataset_cleaned.csv")
BLUE = "#0072B2"       # Okabe-Ito blue
ORANGE = "#E69F00"     # Okabe-Ito orange
GREEN = "#009E73"      # Okabe-Ito bluish green
INK = "#172B3A"


def direction(start: float, end: float) -> str:
    if end > start:
        return "increased"
    if end < start:
        return "decreased"
    return "was unchanged"


@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    data = pd.read_csv(path)
    data.columns = data.columns.str.replace(r"^\*+", "", regex=True).str.strip()
    data["country"] = data["country"].astype("string").str.strip()
    data["year"] = pd.to_numeric(data["year"], errors="coerce")
    data = data.dropna(subset=["country", "year"]).copy()
    data["year"] = data["year"].astype(int)
    return data


st.title("Electric vehicle adoption across countries")
st.caption(
    "How has EV adoption changed, and how does it vary across markets? "
    "Use the filters to explore country and year patterns."
)

try:
    df = load_data(str(DATA_PATH))
except FileNotFoundError:
    st.error(f"Dataset not found: {DATA_PATH.name}. Keep it beside app.py.")
    st.stop()

years = sorted(df["year"].unique().tolist())
countries = sorted(df["country"].dropna().unique().tolist())

with st.sidebar:
    st.header("Explore the data")
    selected_countries = st.multiselect(
        "Countries", countries, default=countries, help="All dashboard views use this selection."
    )
    year_range = st.select_slider(
        "Year range", options=years, value=(years[0], years[-1])
    )
    trend_measure = st.radio(
        "Trend measure", ["EV market share (%)", "EV sales (vehicles)"], horizontal=False
    )

# Compute one shared filtered frame so KPIs and charts stay in sync.
f = df[
    df["country"].isin(selected_countries)
    & df["year"].between(year_range[0], year_range[1])
].copy()

if f.empty:
    st.info("Choose at least one country and a year range containing data.")
    st.stop()

latest_year = int(f["year"].max())
latest = f[f["year"] == latest_year]
mean_share = f["ev_market_share"].mean()
total_ev_sales = f["ev_sales"].sum()

k1, k2, k3 = st.columns(3)
k1.metric("Mean EV market share", f"{mean_share:.1f}%")
k2.metric(f"EV sales, {year_range[0]}–{year_range[1]}", f"{total_ev_sales:,.0f}")
k3.metric("Countries in view", f"{f['country'].nunique():,}")

st.divider()

left, right = st.columns([1.35, 1])
with left:
    if trend_measure == "EV market share (%)":
        trend = f.groupby("year", as_index=False)["ev_market_share"].mean()
        y_col, y_label = "ev_market_share", "Mean EV market share (%)"
    else:
        trend = f.groupby("year", as_index=False)["ev_sales"].sum()
        y_col, y_label = "ev_sales", "EV sales (vehicles)"
    start_value, end_value = trend[y_col].iloc[0], trend[y_col].iloc[-1]
    if trend_measure == "EV market share (%)":
        trend_title = (
            f"Mean EV share {direction(start_value, end_value)} "
            f"from {start_value:.1f}% to {end_value:.1f}%"
        )
    else:
        trend_title = (
            f"EV sales {direction(start_value, end_value)} "
            f"from {start_value:,.0f} to {end_value:,.0f}"
        )
    fig = px.line(
        trend, x="year", y=y_col, markers=True,
        title=trend_title, labels={"year": "Year", y_col: y_label},
        color_discrete_sequence=[BLUE],
    )
    fig.update_traces(hovertemplate="Year %{x}<br>" + y_label + ": %{y:,.2f}<extra></extra>")
    fig.update_layout(margin=dict(l=8, r=8, t=54, b=8), hovermode="x unified", font=dict(size=14, color=INK))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    if trend_measure == "EV market share (%)":
        summary = (
            f"Chart summary: the unweighted mean EV share {direction(start_value, end_value)} "
            f"from {start_value:.2f}% in {int(trend['year'].iloc[0])} to "
            f"{end_value:.2f}% in {int(trend['year'].iloc[-1])}."
        )
    else:
        summary = (
            f"Chart summary: EV sales {direction(start_value, end_value)} from "
            f"{start_value:,.0f} in {int(trend['year'].iloc[0])} to "
            f"{end_value:,.0f} in {int(trend['year'].iloc[-1])}."
        )
    st.caption(summary + " Country means are unweighted by population or vehicle sales.")

with right:
    ranking = latest.groupby("country", as_index=False)["ev_market_share"].mean()
    ranking = ranking.nlargest(10, "ev_market_share").sort_values("ev_market_share")
    leader = ranking.iloc[-1]
    fig = px.bar(
        ranking, x="ev_market_share", y="country", orientation="h",
        title=f"{leader['country']} leads the selected sample in {latest_year}",
        labels={"ev_market_share": "EV market share (%)", "country": "Country"},
        color_discrete_sequence=[GREEN], text_auto=".1f",
    )
    fig.update_layout(margin=dict(l=8, r=8, t=54, b=8), xaxis_rangemode="tozero", font=dict(size=14, color=INK))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.caption(f"Chart summary: {leader['country']} has the highest EV market share in {latest_year} among the selected countries, at {leader['ev_market_share']:.2f}%.")

left, right = st.columns([1, 1])
with left:
    scatter = f[f["charging_stations"] > 0]
    if len(scatter) >= 2 and scatter["charging_stations"].nunique() > 1 and scatter["ev_market_share"].nunique() > 1:
        rho = scatter["charging_stations"].rank().corr(scatter["ev_market_share"].rank())
        relation = "positive" if rho > 0.1 else "negative" if rho < -0.1 else "weak"
        scatter_title = f"{relation.title()} station-count and EV-share association (ρ = {rho:.2f})"
    else:
        rho = float("nan")
        scatter_title = "Station counts and EV share in selected country-years"
    fig = px.scatter(
        scatter, x="charging_stations", y="ev_market_share", hover_name="country",
        hover_data={"year": True, "charging_stations": ":,", "ev_market_share": ":.2f"},
        title=scatter_title,
        labels={"charging_stations": "Charging stations (count)", "ev_market_share": "EV market share (%)"},
        color_discrete_sequence=[ORANGE],
    )
    fig.update_xaxes(type="log", title="Charging stations (count, logarithmic scale)")
    fig.update_layout(margin=dict(l=8, r=8, t=54, b=8), font=dict(size=14, color=INK))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    if pd.notna(rho):
        st.caption(f"Chart summary: each mark is one country-year; the selected rows show a {relation} rank association (Spearman ρ = {rho:.2f}). Zero station counts are omitted on the log scale; this is not causal evidence.")
    else:
        st.caption("Chart summary: each mark is a country-year with a positive station count; this selection has too little variation to summarize an association. The log axis omits zero counts.")

with right:
    emissions = f.groupby("year", as_index=False)["co2_emissions_transport_mt"].mean()
    emissions_start, emissions_end = emissions.iloc[0, 1], emissions.iloc[-1, 1]
    fig = px.line(
        emissions, x="year", y="co2_emissions_transport_mt", markers=True,
        title=f"Mean transport emissions {direction(emissions_start, emissions_end)} from {emissions_start:.1f} to {emissions_end:.1f} Mt",
        labels={"year": "Year", "co2_emissions_transport_mt": "Transport emissions (Mt)"},
        color_discrete_sequence=[INK],
    )
    fig.update_layout(margin=dict(l=8, r=8, t=54, b=8), hovermode="x unified", font=dict(size=14, color=INK))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.caption(f"Chart summary: mean transport emissions {direction(emissions.iloc[0, 1], emissions.iloc[-1, 1])} from {emissions.iloc[0, 1]:.1f} Mt in {int(emissions.iloc[0, 0])} to {emissions.iloc[-1, 1]:.1f} Mt in {int(emissions.iloc[-1, 0])} across the selected countries.")

with st.expander("Drill down to one country's vehicle sales mix"):
    detail_country = st.selectbox("Country detail", sorted(f["country"].unique()))
    detail = f[f["country"] == detail_country].sort_values("year")
    detail_last = detail.iloc[-1]
    fig = px.bar(
        detail, x="year", y=["ev_sales", "petrol_car_sales", "diesel_car_sales"],
        title=f"EV share in {detail_country} reached {detail_last['ev_market_share']:.1f}% in {int(detail_last['year'])}", barmode="stack",
        labels={"year": "Year", "value": "Vehicles sold", "variable": "Vehicle type"},
        color_discrete_map={"ev_sales": BLUE, "petrol_car_sales": ORANGE, "diesel_car_sales": GREEN},
    )
    fig.update_layout(margin=dict(l=8, r=8, t=54, b=8), legend_title_text="Vehicle type", font=dict(size=14, color=INK))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.caption(f"Chart summary: the stacked bars compare EV, petrol and diesel sales in {detail_country} for each year in the selected range.")

st.download_button(
    "Download filtered rows as CSV",
    f.to_csv(index=False).encode("utf-8"),
    file_name="ev_adoption_filtered.csv",
    mime="text/csv",
)

st.caption(
    "Data file: ev_vs_petrol_dataset_cleaned.csv · 400 country-year rows · 25 countries · 2010–2025. "
    "Dataset source and licence are not recorded in the project files."
)
