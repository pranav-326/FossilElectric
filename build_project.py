"""Rebuild the country-year dataset and the four frozen project charts."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "ev_vs_petrol_dataset_v3-selected-columns.csv"
CLEAN = ROOT / "ev_vs_petrol_dataset_cleaned.csv"
FIGS = ROOT / "figs"

SALES = ["ev_sales", "petrol_car_sales", "diesel_car_sales"]
SHARED = [
    "charging_stations",
    "avg_ev_range_km",
    "fuel_price_usd_per_liter",
    "electricity_price_usd_per_kwh",
    "co2_emissions_transport_mt",
    "ev_subsidy_usd",
    "emission_regulation_score",
]
NUMERIC = [
    "year", *SALES, "total_vehicle_sales", "ev_market_share", *SHARED,
    "ev_growth_rate_yoy", "is_ev_dominant",
]
BLUE = "#0072B2"
ORANGE = "#E69F00"
GREEN = "#009E73"
INK = "#172B3A"
GRID = "#E4EBF0"


def prepare_data() -> tuple[pd.DataFrame, dict]:
    raw = pd.read_csv(SOURCE)
    raw.columns = (
        raw.columns.astype(str)
        .str.replace(r"^\*+", "", regex=True)
        .str.replace("&#x66;", "f", regex=False)
        .str.strip()
    )
    raw["country"] = raw["country"].astype("string").str.strip()
    for column in NUMERIC:
        if column in raw:
            raw[column] = pd.to_numeric(raw[column], errors="coerce")

    source_rows = len(raw)
    exact_duplicates = int(raw.duplicated().sum())
    missing_identifiers = int(raw[["country", "year"]].isna().any(axis=1).sum())
    raw = raw.dropna(subset=["country", "year"]).copy()
    raw["year"] = raw["year"].astype(int)

    grouped = raw.groupby(["country", "year"], sort=True, dropna=False)
    # These fields are retained once per country-year only when the source values agree.
    varying_shared = {
        column: int((grouped[column].nunique(dropna=False) > 1).sum())
        for column in SHARED
    }
    if any(varying_shared.values()):
        raise ValueError(
            "A country-year has conflicting shared metrics. Review the source before aggregating: "
            + str(varying_shared)
        )

    result = grouped[SALES].sum().reset_index()
    shared = grouped[SHARED].first().reset_index(drop=True)
    result = pd.concat([result, shared], axis=1)
    result["total_vehicle_sales"] = result[SALES].sum(axis=1)
    result["ev_market_share"] = (
        result["ev_sales"] / result["total_vehicle_sales"] * 100
    ).round(2)
    result = result.sort_values(["country", "year"]).reset_index(drop=True)
    result["ev_growth_rate_yoy"] = (
        result.groupby("country")["ev_sales"].pct_change() * 100
    ).replace([float("inf"), -float("inf")], float("nan"))
    result["is_ev_dominant"] = (result["ev_market_share"] >= 50).astype(int)
    result = result[
        [
            "country", "year", *SALES, "total_vehicle_sales", "ev_market_share",
            *SHARED, "ev_growth_rate_yoy", "is_ev_dominant",
        ]
    ]

    key_duplicates = int(result.duplicated(["country", "year"]).sum())
    if key_duplicates:
        raise ValueError(f"The analysis table still has {key_duplicates} duplicate country-year keys")
    if (result[SALES + ["charging_stations"]] < 0).any().any():
        raise ValueError("Negative sales or charging-station counts require review")
    if not result["ev_market_share"].between(0, 100).all():
        raise ValueError("EV market share is outside 0–100 percent")
    if not (
        result["total_vehicle_sales"]
        == result[SALES].sum(axis=1)
    ).all():
        raise ValueError("Total vehicle sales do not equal the sum of vehicle types")

    CLEAN.write_text(result.to_csv(index=False, lineterminator="\r\n").rstrip("\r\n"), encoding="utf-8", newline="")
    stats = {
        "source_rows": source_rows,
        "analysis_rows": len(result),
        "country_count": int(result["country"].nunique()),
        "year_min": int(result["year"].min()),
        "year_max": int(result["year"].max()),
        "exact_duplicate_source_rows": exact_duplicates,
        "source_rows_missing_country_or_year": missing_identifiers,
        "source_rows_aggregated_into_country_year": source_rows - missing_identifiers - len(result),
        "country_year_key_duplicates_after_aggregation": key_duplicates,
        "missing_growth_values": int(result["ev_growth_rate_yoy"].isna().sum()),
        "missing_values_by_column": result.isna().sum().astype(int).to_dict(),
        "shared_metrics_with_within_key_conflicts": varying_shared,
    }
    print("Rebuilt analysis dataset:", stats)
    print("No IQR candidates are deleted. Candidate counts (1.5 × IQR):")
    for column in ["ev_market_share", "charging_stations", "co2_emissions_transport_mt", "ev_sales"]:
        q1, q3 = result[column].quantile([0.25, 0.75])
        iqr = q3 - q1
        candidates = int(((result[column] < q1 - 1.5 * iqr) | (result[column] > q3 + 1.5 * iqr)).sum())
        print(f"  {column}: {candidates}")
    return result, stats


def style_axis(ax):
    ax.grid(axis="y", color=GRID, linewidth=0.7)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0, colors=INK, labelsize=10)
    ax.tick_params(axis="x", colors=INK, labelsize=10)
    ax.title.set_color(INK)
    ax.xaxis.label.set_color(INK)
    ax.yaxis.label.set_color(INK)


def export_charts(df: pd.DataFrame) -> None:
    FIGS.mkdir(exist_ok=True)
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "axes.titlesize": 15,
        "axes.titleweight": "bold",
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
    })

    trend = df.groupby("year", as_index=False)["ev_market_share"].mean()
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(trend["year"], trend["ev_market_share"], color=BLUE, linewidth=2.5, marker="o", markersize=4)
    ax.set(title="Mean EV market share rose to 21.67% in 2025", xlabel="Year", ylabel="Unweighted mean EV market share (%)")
    ax.set_ylim(bottom=0)
    style_axis(ax)
    last = trend.iloc[-1]
    ax.annotate(f"{last['ev_market_share']:.2f}%", (last["year"], last["ev_market_share"]),
                xytext=(-8, 12), textcoords="offset points", ha="right", color=INK, weight="bold")
    fig.tight_layout()
    fig.savefig(FIGS / "ev_market_share_trend.png", dpi=180,
                metadata={"Description": "The unweighted mean EV market share across 25 countries rises from 0.03 percent in 2010 to 21.67 percent in 2025."})
    plt.close(fig)

    latest_year = int(df["year"].max())
    top = df[df["year"] == latest_year].nlargest(10, "ev_market_share").sort_values("ev_market_share")
    fig, ax = plt.subplots(figsize=(9, 5))
    colors = [BLUE if country == "Norway" else "#78AFCB" for country in top["country"]]
    bars = ax.barh(top["country"], top["ev_market_share"], color=colors, height=0.68)
    ax.set(title=f"Norway led the country sample in {latest_year}", xlabel="EV market share (%)", ylabel="")
    ax.set_xlim(0, max(85, float(top["ev_market_share"].max()) * 1.16))
    style_axis(ax)
    ax.grid(axis="x", color=GRID, linewidth=0.7)
    ax.grid(axis="y", visible=False)
    ax.bar_label(bars, fmt="%.1f%%", padding=4, fontsize=9, color=INK)
    fig.tight_layout()
    leader = top.iloc[-1]
    fig.savefig(FIGS / "ev_market_share_ranking.png", dpi=180,
                metadata={"Description": f"A sorted bar chart ranks the ten highest country EV market shares in {latest_year}; {leader['country']} leads at {leader['ev_market_share']:.2f} percent."})
    plt.close(fig)

    scatter = df[df["charging_stations"] > 0]
    rho = scatter["charging_stations"].rank().corr(scatter["ev_market_share"].rank())
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.scatter(scatter["charging_stations"], scatter["ev_market_share"], color=ORANGE, s=28, alpha=0.68, edgecolors="none")
    ax.set_xscale("log")
    ax.set(title="Station counts and EV share align in pooled records",
           xlabel="Charging stations (count, logarithmic scale)", ylabel="EV market share (%)")
    style_axis(ax)
    ax.grid(axis="x", color=GRID, linewidth=0.7, which="both")
    ax.text(0.01, -0.23, f"Each point is one country-year; Spearman ρ = {rho:.2f}. Zero counts are omitted on the log scale. Association is not causal evidence.",
            transform=ax.transAxes, fontsize=9, color=INK)
    fig.tight_layout()
    fig.savefig(FIGS / "charging_stations_vs_ev_share.png", dpi=180,
                metadata={"Description": f"A scatter plot compares charging stations and EV market share for country-years with positive station counts; the Spearman rank correlation is {rho:.2f}, which is descriptive and not causal."})
    plt.close(fig)

    emissions = df.groupby("year", as_index=False)["co2_emissions_transport_mt"].mean()
    peak = emissions.loc[emissions["co2_emissions_transport_mt"].idxmax()]
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(emissions["year"], emissions["co2_emissions_transport_mt"], color=GREEN, linewidth=2.5, marker="o", markersize=4)
    ax.set(title=f"Mean transport emissions peaked in {int(peak['year'])}", xlabel="Year", ylabel="Unweighted mean transport emissions (Mt)")
    ax.set_ylim(bottom=0)
    style_axis(ax)
    ax.annotate(f"Peak: {peak['co2_emissions_transport_mt']:.1f} Mt",
                (peak["year"], peak["co2_emissions_transport_mt"]), xytext=(16, -22),
                textcoords="offset points", va="top", color=INK, weight="bold",
                arrowprops={"arrowstyle": "->", "color": INK, "lw": 0.9})
    fig.tight_layout()
    fig.savefig(FIGS / "transport_emissions_trend.png", dpi=180,
                metadata={"Description": f"The unweighted mean of transport emissions across the selected country sample peaks in {int(peak['year'])} at {peak['co2_emissions_transport_mt']:.1f} million tonnes."})
    plt.close(fig)
    print(f"Exported four labelled chart files to {FIGS}")


if __name__ == "__main__":
    data, _ = prepare_data()
    export_charts(data)
