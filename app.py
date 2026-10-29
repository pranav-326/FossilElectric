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
        finding = "Average EV market share rose across the selected countries"
    else:
        trend = f.groupby("year", as_index=False)["ev_sales"].sum()
        y_col, y_label = "ev_sales", "EV sales (vehicles)"
        finding = "EV sales increased across the selected countries"
    fig = px.line(
        trend, x="year", y=y_col, markers=True,
        title=finding, labels={"year": "Year", y_col: y_label},
        color_discrete_sequence=[BLUE],
    )
    fig.update_traces(hovertemplate="Year %{x}<br>" + y_label + ": %{y:,.2f}<extra></extra>")
    fig.update_layout(margin=dict(l=8, r=8, t=54, b=8), hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.caption("Trend is a simple mean by country-year; it is not weighted by population or vehicle sales.")

with right:
    ranking = latest.groupby("country", as_index=False)["ev_market_share"].mean()
    ranking = ranking.nlargest(10, "ev_market_share").sort_values("ev_market_share")
    fig = px.bar(
        ranking, x="ev_market_share", y="country", orientation="h",
        title=f"Highest EV market shares in {latest_year}",
        labels={"ev_market_share": "EV market share (%)", "country": "Country"},
        color_discrete_sequence=[GREEN], text_auto=".1f",
    )
    fig.update_layout(margin=dict(l=8, r=8, t=54, b=8), xaxis_rangemode="tozero")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

left, right = st.columns([1, 1])
with left:
    scatter = f[f["charging_stations"] > 0]
    fig = px.scatter(
        scatter, x="charging_stations", y="ev_market_share", hover_name="country",
        hover_data={"year": True, "charging_stations": ":,", "ev_market_share": ":.2f"},
        title="Charging network and EV market share",
        labels={"charging_stations": "Charging stations (count)", "ev_market_share": "EV market share (%)"},
        color_discrete_sequence=[ORANGE],
    )
    fig.update_xaxes(type="log", title="Charging stations (count, logarithmic scale)")
    fig.update_layout(margin=dict(l=8, r=8, t=54, b=8))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.caption("Each mark is one country-year with a positive station count; zero counts are omitted on the log scale. Association is not causation.")

with right:
    emissions = f.groupby("year", as_index=False)["co2_emissions_transport_mt"].mean()
    fig = px.line(
        emissions, x="year", y="co2_emissions_transport_mt", markers=True,
        title="Mean transport emissions across selected countries",
        labels={"year": "Year", "co2_emissions_transport_mt": "Transport emissions (Mt)"},
        color_discrete_sequence=[INK],
    )
    fig.update_layout(margin=dict(l=8, r=8, t=54, b=8), hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with st.expander("Drill down to one country's vehicle sales mix"):
    detail_country = st.selectbox("Country detail", sorted(f["country"].unique()))
    detail = f[f["country"] == detail_country].sort_values("year")
    fig = px.bar(
        detail, x="year", y=["ev_sales", "petrol_car_sales", "diesel_car_sales"],
        title=f"Vehicle sales by type in {detail_country}", barmode="stack",
        labels={"year": "Year", "value": "Vehicles sold", "variable": "Vehicle type"},
        color_discrete_map={"ev_sales": BLUE, "petrol_car_sales": ORANGE, "diesel_car_sales": GREEN},
    )
    fig.update_layout(margin=dict(l=8, r=8, t=54, b=8), legend_title_text="Vehicle type")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

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
