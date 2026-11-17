"""
⚡ FossilElectric — Electric Vehicle Data Visualization & Analytics Platform
A commercial-grade executive data analytics platform comparing electric vehicle adoption,
infrastructure, and fuel displacement across 25 global sovereign markets (2010–2025).
"""

from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ──────────────────────────────────────────────────────────────────────────────
# 1. PAGE SETUP
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FossilElectric · EV Market Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_PATH = Path(__file__).with_name("ev_vs_petrol_dataset_cleaned.csv")

# ──────────────────────────────────────────────────────────────────────────────
# 2. COLOR PALETTE & LABELS
# ──────────────────────────────────────────────────────────────────────────────
COLORS = {
    "primary": "#2563EB",       # Royal Cobalt
    "ev": "#2563EB",            # EV Blue
    "petrol": "#D97706",        # Petrol Amber-600
    "diesel": "#64748B",        # Diesel Slate-500
    "green": "#059669",         # Emerald-600
    "red": "#E11D48",           # Rose-600
    "purple": "#6366F1",        # Indigo-500
    "slate_dark": "#0B0F19",    # Deep Charcoal
    "slate_text": "#334155",    # Slate-700
    "slate_muted": "#64748B",   # Slate-500
    "border": "#E2E8F0",        # Slate-200
    "card_bg": "#FFFFFF",       # Pure White
    "canvas": "#F8FAFC",        # Slate-50
    "grid": "#F1F5F9",          # Slate-100
}

CHART_PALETTE = [
    "#2563EB", "#059669", "#D97706", "#6366F1", "#0284C7",
    "#DB2777", "#D97706", "#0D9488", "#4F46E5", "#65A30D",
    "#C026D3", "#CA8A04", "#0369A1", "#047857", "#BE123C",
]

REGION_MAP = {
    "Australia": "Asia-Pacific", "Austria": "Europe", "Belgium": "Europe",
    "Brazil": "Americas", "Canada": "Americas", "China": "Asia-Pacific",
    "France": "Europe", "Germany": "Europe", "India": "Asia-Pacific",
    "Indonesia": "Asia-Pacific", "Italy": "Europe", "Japan": "Asia-Pacific",
    "Mexico": "Americas", "Netherlands": "Europe", "Norway": "Europe",
    "Poland": "Europe", "Portugal": "Europe", "South Korea": "Asia-Pacific",
    "Spain": "Europe", "Sweden": "Europe", "Switzerland": "Europe",
    "Thailand": "Asia-Pacific", "Turkey": "Europe", "United Kingdom": "Europe",
    "United States": "Americas",
}

FEATURE_LABELS = {
    "country": "Country",
    "year": "Year",
    "region": "Geographic Region",
    "ev_market_share": "EV Market Share (%)",
    "ev_sales": "Annual EV Sales (Units)",
    "petrol_car_sales": "Petrol Vehicle Sales",
    "diesel_car_sales": "Diesel Vehicle Sales",
    "total_vehicle_sales": "Total Vehicle Sales",
    "charging_stations": "Public Charging Stations",
    "avg_ev_range_km": "Avg. Battery Range (km)",
    "fuel_price_usd_per_liter": "Petrol Price ($/Litre)",
    "electricity_price_usd_per_kwh": "Electricity Price ($/kWh)",
    "co2_emissions_transport_mt": "Transport CO₂ Emissions (Mt)",
    "ev_subsidy_usd": "Government Subsidy ($/EV)",
    "emission_regulation_score": "Emission Regulation Score (0–100)",
    "fuel_cost_100km": "Petrol Fuel Cost ($/100km)",
    "ev_cost_100km": "EV Electricity Cost ($/100km)",
    "savings_100km": "Fuel Cost Savings ($/100km)",
    "annual_savings": "Annual Fuel Savings ($/Driver)",
    "chargers_per_1k_ev": "Chargers per 1,000 EVs",
}

def label_of(k: str) -> str:
    return FEATURE_LABELS.get(k, k.replace("_", " ").title())


# ──────────────────────────────────────────────────────────────────────────────
# 3. COMMERCIAL SAAS DESIGN SYSTEM (INTER + JETBRAINS MONO, REFINED PALETTE)
# ──────────────────────────────────────────────────────────────────────────────
def inject_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* Global Typography Reset & Antialiasing (Preserving Streamlit Icons) */
    html, body, .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        -webkit-font-smoothing: antialiased !important;
        -moz-osx-font-smoothing: grayscale !important;
        font-feature-settings: "cv02", "cv03", "cv04", "cv11", "tnum" !important;
    }

    /* Preserve Material Symbols & Icons for Sidebar Collapse/Expand buttons */
    span[data-testid="stIconMaterial"],
    .material-symbols-rounded,
    [data-testid="stSidebarCollapseButton"] *,
    [data-testid="collapsedControl"] *,
    button[kind="header"] * {
        font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
    }

    /* Canvas background */
    .stApp {
        background-color: #F8FAFC !important;
    }

    .main .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 4rem !important;
        max-width: 1400px !important;
    }

    /* ── SIDEBAR (DEEP CHARCOAL SLATE, PROFESSIONAL SaaS) ── */
    section[data-testid="stSidebar"] {
        background-color: #0B0F19 !important;
        border-right: 1px solid #1E293B !important;
    }

    .sidebar-brand-wrapper {
        padding: 0.25rem 0 1.25rem 0;
        border-bottom: 1px solid #1E293B;
        margin-bottom: 1.25rem;
    }

    .brand-badge {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: rgba(37, 99, 235, 0.15);
        border: 1px solid rgba(59, 130, 246, 0.3);
        color: #60A5FA;
        font-size: 0.65rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        padding: 2px 7px;
        border-radius: 4px;
        margin-bottom: 0.45rem;
    }

    .brand-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #FFFFFF !important;
        letter-spacing: -0.02em;
        line-height: 1.2;
        margin: 0;
    }

    .brand-desc {
        font-size: 0.74rem;
        color: #94A3B8;
        margin-top: 0.25rem;
        line-height: 1.35;
    }

    /* Sidebar Radio Navigation Items */
    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] {
        gap: 0.3rem;
    }

    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label {
        background: transparent !important;
        border-radius: 6px !important;
        padding: 0.55rem 0.8rem !important;
        cursor: pointer !important;
        transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 100% !important;
        border: 1px solid transparent !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child {
        display: none !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label:hover {
        background: rgba(255, 255, 255, 0.05) !important;
        border-color: rgba(255, 255, 255, 0.08) !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) {
        background: #1E293B !important;
        border: 1px solid #334155 !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2) !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label p {
        color: #94A3B8 !important;
        font-size: 0.88rem !important;
        font-weight: 500 !important;
        margin: 0 !important;
        transition: color 0.15s ease !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label:hover p {
        color: #F1F5F9 !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) p {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    /* Sidebar Metadata Footer Card */
    .sidebar-meta-card {
        margin-top: 2.5rem;
        padding: 0.85rem 1rem;
        background: #111827;
        border: 1px solid #1F2937;
        border-radius: 8px;
    }

    .meta-status-row {
        display: flex;
        align-items: center;
        gap: 6px;
        margin-bottom: 0.45rem;
    }

    .status-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background-color: #10B981;
        box-shadow: 0 0 6px #10B981;
    }

    .status-text {
        font-size: 0.68rem;
        font-weight: 700;
        color: #E2E8F0;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    .meta-details {
        font-size: 0.72rem;
        color: #94A3B8;
        line-height: 1.45;
    }

    /* ── PAGE HEADERS & BREADCRUMBS ── */
    .page-header-container {
        margin-bottom: 1.75rem;
        padding-bottom: 1.25rem;
        border-bottom: 1px solid #E2E8F0;
    }

    .page-eyebrow {
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #2563EB;
        margin-bottom: 0.35rem;
    }

    .page-title {
        font-size: 1.75rem;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.03em;
        line-height: 1.2;
        margin: 0 0 0.4rem 0;
    }

    .page-desc {
        font-size: 0.92rem;
        color: #64748B;
        margin: 0;
        line-height: 1.5;
    }

    /* ── TOP KPI METRIC CARDS ── */
    .kpi-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1.25rem 1.35rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.02);
        position: relative;
        overflow: hidden;
        height: 100%;
    }

    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2.5px;
        background: #CBD5E1;
    }

    .kpi-card.accent-blue::before { background: #2563EB; }
    .kpi-card.accent-emerald::before { background: #059669; }
    .kpi-card.accent-indigo::before { background: #6366F1; }
    .kpi-card.accent-amber::before { background: #D97706; }

    .kpi-label {
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #64748B;
        margin-bottom: 0.4rem;
    }

    .kpi-value {
        font-size: 2rem;
        font-weight: 800;
        color: #0F172A;
        line-height: 1.1;
        letter-spacing: -0.03em;
        font-feature-settings: 'tnum';
        margin-bottom: 0.45rem;
    }

    .kpi-delta-pill {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        font-size: 0.74rem;
        font-weight: 600;
        padding: 2px 7px;
        border-radius: 4px;
        background: #ECFDF5;
        color: #059669;
        border: 1px solid #A7F3D0;
    }

    .kpi-subtext {
        font-size: 0.76rem;
        color: #64748B;
        margin-top: 0.25rem;
    }

    /* ── EXECUTIVE BRIEFING DIGEST ── */
    .digest-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 3.5px solid #2563EB;
        border-radius: 8px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
    }

    .digest-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.85rem;
        padding-bottom: 0.6rem;
        border-bottom: 1px solid #F1F5F9;
    }

    .digest-title {
        font-size: 0.82rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        color: #1E3A8A;
        margin: 0;
    }

    .digest-badge {
        font-size: 0.68rem;
        font-weight: 600;
        color: #2563EB;
        background: #EFF6FF;
        border: 1px solid #DBEAFE;
        padding: 2px 7px;
        border-radius: 4px;
    }

    .digest-list {
        margin: 0;
        padding: 0;
        list-style: none;
        display: flex;
        flex-direction: column;
        gap: 0.55rem;
    }

    .digest-list li {
        font-size: 0.85rem;
        line-height: 1.55;
        color: #334155;
        position: relative;
        padding-left: 1.25rem;
    }

    .digest-list li::before {
        content: "■";
        position: absolute;
        left: 0;
        top: -1px;
        color: #2563EB;
        font-size: 0.65rem;
    }

    .digest-list li b {
        color: #0F172A;
    }

    /* ── UNIFIED SAAS CHART PANELS (BORDER WRAPPERS) ── */
    div[data-testid="stVerticalBlockBorderWrapper"] > div {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02) !important;
        padding: 1.25rem !important;
    }

    .chart-meta-overline {
        font-size: 0.65rem;
        font-weight: 700;
        letter-spacing: 0.07em;
        text-transform: uppercase;
        color: #2563EB;
        margin-bottom: 0.25rem;
    }

    .chart-title-text {
        font-size: 0.95rem;
        font-weight: 700;
        color: #0F172A;
        letter-spacing: -0.015em;
        margin: 0 0 0.25rem 0;
        line-height: 1.3;
    }

    .chart-desc-text {
        font-size: 0.77rem;
        color: #64748B;
        margin: 0 0 0.85rem 0;
        line-height: 1.4;
    }

    .chart-takeaway-box {
        background: #F8FAFC;
        border-top: 1px solid #F1F5F9;
        padding: 0.7rem 0.85rem;
        margin-top: 0.5rem;
        border-radius: 6px;
        font-size: 0.8rem;
        color: #475569;
        line-height: 1.45;
    }

    .chart-takeaway-box b {
        color: #0F172A;
    }

    /* ── BULLETPROOF HIGH-CONTRAST SELECTBOX & INPUT SYSTEM ── */
    div[data-testid="stSelectbox"] label p,
    div[data-testid="stMultiSelect"] label p,
    div[data-testid="stTextInput"] label p {
        color: #0F172A !important;
        font-weight: 700 !important;
        font-size: 0.86rem !important;
        letter-spacing: -0.01em !important;
    }

    div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        border-radius: 6px !important;
    }

    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 6px !important;
        min-height: 40px !important;
    }

    div[data-baseweb="select"] *,
    div[data-baseweb="select"] div,
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] input,
    div[data-baseweb="select"] [role="combobox"],
    div[data-testid="stSelectbox"] [data-baseweb="select"] div,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] * {
        color: #0F172A !important;
        -webkit-text-fill-color: #0F172A !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        opacity: 1 !important;
    }

    div[data-baseweb="tag"] {
        background-color: #2563EB !important;
        border-radius: 5px !important;
        padding: 2px 7px !important;
    }

    div[data-baseweb="tag"] *,
    div[data-baseweb="tag"] span {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 0.8rem !important;
    }

    div[data-baseweb="tag"] svg {
        fill: #FFFFFF !important;
        color: #FFFFFF !important;
    }

    div[data-baseweb="popover"],
    div[data-baseweb="popover"] *,
    div[data-baseweb="menu"],
    div[data-baseweb="menu"] *,
    ul[role="listbox"],
    ul[role="listbox"] * {
        color: #0F172A !important;
        -webkit-text-fill-color: #0F172A !important;
        background-color: #FFFFFF !important;
    }

    li[role="option"] {
        background-color: #FFFFFF !important;
        padding: 8px 12px !important;
    }

    li[role="option"]:hover,
    li[role="option"][aria-selected="true"] {
        background-color: #EFF6FF !important;
    }

    li[role="option"]:hover *,
    li[role="option"][aria-selected="true"] * {
        color: #2563EB !important;
        -webkit-text-fill-color: #2563EB !important;
        font-weight: 700 !important;
    }

    /* ── SAAS BUTTON SYSTEM ── */
    div[data-testid="stButton"] > button {
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        color: #0F172A !important;
        font-size: 0.84rem !important;
        font-weight: 600 !important;
        border-radius: 6px !important;
        padding: 0.45rem 0.9rem !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04) !important;
        transition: all 0.15s ease !important;
    }

    div[data-testid="stButton"] > button:hover {
        border-color: #94A3B8 !important;
        background-color: #F8FAFC !important;
        color: #2563EB !important;
    }

    div[data-testid="stButton"] > button:active {
        transform: translateY(1px) !important;
    }

    div[data-testid="stDownloadButton"] > button {
        background-color: #2563EB !important;
        border: 1px solid #1D4ED8 !important;
        color: #FFFFFF !important;
        font-size: 0.86rem !important;
        font-weight: 600 !important;
        border-radius: 6px !important;
        padding: 0.5rem 1.1rem !important;
        box-shadow: 0 1px 2px rgba(37, 99, 235, 0.2) !important;
        transition: all 0.15s ease !important;
    }

    div[data-testid="stDownloadButton"] > button:hover {
        background-color: #1D4ED8 !important;
        border-color: #1E40AF !important;
        color: #FFFFFF !important;
    }

    /* ── SLEEK TABS ── */
    div[data-baseweb="tab-list"] {
        gap: 1.5rem !important;
        background-color: transparent !important;
        border-bottom: 1px solid #E2E8F0 !important;
        padding-bottom: 0px !important;
        margin-bottom: 1.5rem !important;
    }

    div[data-baseweb="tab"] {
        background-color: transparent !important;
        color: #64748B !important;
        font-size: 0.92rem !important;
        font-weight: 500 !important;
        padding: 0.6rem 0.25rem 0.75rem 0.25rem !important;
        border-bottom: 2px solid transparent !important;
        transition: all 0.15s ease !important;
    }

    div[data-baseweb="tab"]:hover {
        color: #0F172A !important;
    }

    div[data-baseweb="tab"][aria-selected="true"] {
        color: #2563EB !important;
        font-weight: 700 !important;
        border-bottom: 2px solid #2563EB !important;
    }

    /* ── FOOTER ── */
    .footer {
        text-align: center;
        padding: 2.5rem 0 1rem 0;
        color: #94A3B8;
        font-size: 0.78rem;
        border-top: 1px solid #E2E8F0;
        margin-top: 3.5rem;
    }
    </style>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# 4. DATA ENGINE
# ──────────────────────────────────────────────────────────────────────────────
@st.cache_data
def get_clean_data(path_str: str) -> pd.DataFrame:
    df = pd.read_csv(path_str)
    df.columns = df.columns.str.strip()
    df["country"] = df["country"].str.strip()
    df["region"] = df["country"].map(REGION_MAP).fillna("Other")

    # Domain Derived Metrics
    # 1. Fuel cost per 100 km (Assume 8.0 L / 100 km for petrol ICE)
    df["fuel_cost_100km"] = df["fuel_price_usd_per_liter"] * 8.0
    # 2. EV electricity cost per 100 km (Assume 18.0 kWh / 100 km)
    df["ev_cost_100km"] = df["electricity_price_usd_per_kwh"] * 18.0
    # 3. Direct fuel savings per 100 km
    df["savings_100km"] = (df["fuel_cost_100km"] - df["ev_cost_100km"]).clip(lower=0)
    # 4. Annual savings (assuming 15,000 km driven / year)
    df["annual_savings"] = df["savings_100km"] * 150.0
    # 5. Public charging ratio (chargers per 1,000 EVs)
    df["chargers_per_1k_ev"] = np.where(
        df["ev_sales"] > 0,
        (df["charging_stations"] / df["ev_sales"]) * 1000.0,
        0.0
    )
    return df


def fmt_val(v) -> str:
    """Format numerical values compactly with tabular numbers."""
    if pd.isna(v):
        return "N/A"
    abs_v = abs(v)
    if abs_v >= 1e9:
        return f"{v/1e9:.2f}B"
    if abs_v >= 1e6:
        return f"{v/1e6:.2f}M"
    if abs_v >= 1e3:
        return f"{v/1e3:.1f}k"
    return f"{v:,.1f}" if isinstance(v, float) else f"{v:,}"


def clean_plot_layout(height=340, show_legend=True):
    """Refined, crisp Plotly layout matching commercial SaaS standards."""
    return dict(
        height=height,
        margin=dict(l=45, r=20, t=25, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, -apple-system, sans-serif", size=11, color="#475569"),
        showlegend=show_legend,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=10, color="#64748B"),
        ),
        xaxis=dict(gridcolor="#F1F5F9", zeroline=False),
        yaxis=dict(gridcolor="#F1F5F9", zeroline=False),
        hoverlabel=dict(
            bgcolor="#0F172A",
            font_size=12,
            font_family="Inter, sans-serif",
            font_color="#FFFFFF",
            bordercolor="#334155",
        ),
    )

PLOT_CONFIG = {
    "displayModeBar": True,
    "displaylogo": False,
    "doubleClick": "reset+autosize",
    "modeBarButtonsToAdd": ["resetViews", "autoScale2d"],
    "modeBarButtonsToRemove": ["lasso2d", "select2d"],
    "scrollZoom": False,
}


# ──────────────────────────────────────────────────────────────────────────────
# 5. INITIALIZE DATA & SIDEBAR NAVIGATION
# ──────────────────────────────────────────────────────────────────────────────
inject_custom_css()

try:
    df = get_clean_data(str(DATA_PATH))
except FileNotFoundError:
    st.error(f"Dataset not found: {DATA_PATH.name}. Make sure it is in the project directory.")
    st.stop()

all_years = sorted(df["year"].unique().tolist())
all_countries = sorted(df["country"].unique().tolist())
# Strictly 3 canonical continental regions
all_regions = ["Europe", "Asia-Pacific", "Americas"]
latest_yr = int(df["year"].max())
earliest_yr = int(df["year"].min())

df_latest = df[df["year"] == latest_yr]
df_earliest = df[df["year"] == earliest_yr]

with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand-wrapper">
        <div class="brand-title">⚡ FossilElectric</div>
        <div class="brand-desc">Global EV Market Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        [
            "📊 Dashboard Overview",
            "🛠️ Custom Chart Studio",
            "👥 Country Comparisons",
            "📋 Data Table & Export",
        ],
        label_visibility="collapsed",
    )

    st.markdown("""
    <div class="sidebar-meta-card">
        <div class="meta-status-row">
            <div class="status-dot"></div>
            <div class="status-text">Live Intelligence</div>
        </div>
        <div class="meta-details">
            <b>25 Sovereign Markets</b><br>
            400 Verified Observations<br>
            Temporal Scope: 2010–2025<br>
            <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; color: #64748B;">Dataset: cleaned.csv</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1: 📊 DASHBOARD OVERVIEW (EXPANDED TO 12 HIGH-VALUE CHARTS)
# ══════════════════════════════════════════════════════════════════════════════
if page == "📊 Dashboard Overview":
    st.markdown(f"""
    <div class="page-header-container">
        <div class="page-eyebrow">MARKET INTELLIGENCE / EXECUTIVE OVERVIEW</div>
        <div class="page-title">Global Electric Vehicle Transition</div>
        <div class="page-desc">Executive market intelligence tracking EV adoption, infrastructure scale, policy incentives, and fleet displacement across 25 sovereign economies ({earliest_yr}–{latest_yr}).</div>
    </div>
    """, unsafe_allow_html=True)

    # 4 Key Metrics
    mean_share = df_latest["ev_market_share"].mean()
    total_evs = df_latest["ev_sales"].sum()
    top_nation = df_latest.loc[df_latest["ev_market_share"].idxmax()]
    avg_range = df_latest["avg_ev_range_km"].mean()

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="kpi-card accent-blue">
            <div class="kpi-label">Market Share ({latest_yr})</div>
            <div class="kpi-value">{mean_share:.1f}%</div>
            <div class="kpi-delta-pill">↑ +{mean_share - df_earliest['ev_market_share'].mean():.1f}% vs {earliest_yr}</div>
            <div class="kpi-subtext">Weighted across 25 economies</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="kpi-card accent-emerald">
            <div class="kpi-label">Total EVs Sold ({latest_yr})</div>
            <div class="kpi-value">{fmt_val(total_evs)}</div>
            <div class="kpi-delta-pill">Physical Volume</div>
            <div class="kpi-subtext">Combined across 25 nations</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="kpi-card accent-indigo">
            <div class="kpi-label">Global Leader ({latest_yr})</div>
            <div class="kpi-value">{top_nation['country']}</div>
            <div class="kpi-delta-pill">{top_nation['ev_market_share']:.1f}% Share</div>
            <div class="kpi-subtext">Highest sovereign penetration</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="kpi-card accent-amber">
            <div class="kpi-label">Average Range ({latest_yr})</div>
            <div class="kpi-value">{avg_range:.0f} km</div>
            <div class="kpi-delta-pill">↑ +{avg_range - df_earliest['avg_ev_range_km'].mean():.0f} km vs {earliest_yr}</div>
            <div class="kpi-subtext">Single-charge autonomy</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div style="height: 18px;"></div>', unsafe_allow_html=True)

    # Executive Briefing
    st.markdown("""
    <div class="digest-card">
        <div class="digest-header">
            <div class="digest-title">Institutional Briefing · Strategic Findings</div>
            <span class="digest-badge">Global Transition Index</span>
        </div>
        <ul class="digest-list">
            <li><b>Accelerating Adoption:</b> Average global EV market share reached <b>21.8% in 2025</b>, up from less than 0.2% in 2010. Norway leads the world with an 88.5% share.</li>
            <li><b>Parity Milestone:</b> Average single-charge battery range reached <b>480 km in 2025</b>, effectively eliminating consumer range anxiety for daily travel.</li>
            <li><b>Operating Economy:</b> Operating an electric vehicle saves drivers an average of <b>67% on energy costs</b> compared to petrol (~$1,000/year over 15,000 km).</li>
            <li><b>Infrastructure Scale:</b> Over 8.1 million public charging points have been installed worldwide across the 25 surveyed economies.</li>
            <li><b>Decarbonization Impact:</b> Road transport CO₂ emissions have peaked across early-adopting economies as retiring internal combustion cars are replaced by electric powertrains.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Row 1: Global Trend & Top 10 Leaders
    c1, c2 = st.columns(2)

    with c1:
        with st.container(border=True):
            st.markdown("""
            <div class="chart-meta-overline">METRIC #01 · ADOPTION VELOCITY</div>
            <div class="chart-title-text">1. Global EV Market Share Progression (2010–2025)</div>
            <div class="chart-desc-text">Mean percentage of total new passenger vehicle registrations that are battery electric or plug-in hybrid</div>
            """, unsafe_allow_html=True)

            yr_trend = df.groupby("year", as_index=False)["ev_market_share"].mean()
            fig_trend = px.line(
                yr_trend, x="year", y="ev_market_share",
                markers=True, color_discrete_sequence=[COLORS["ev"]],
                labels={"year": "Year", "ev_market_share": "Avg. EV Share (%)"},
            )
            fig_trend.update_traces(
                line=dict(width=3), marker=dict(size=7),
                hovertemplate="<b>Year:</b> %{x}<br>Average EV Share: <b>%{y:.1f}%</b><extra></extra>",
            )
            fig_trend.update_layout(**clean_plot_layout(height=300, show_legend=False))
            st.plotly_chart(fig_trend, use_container_width=True, config=PLOT_CONFIG)

            st.markdown(f"""
            <div class="chart-takeaway-box">
                <b>Analyst Finding:</b> EV market share followed an exponential S-curve, breaking the critical 5% mass-adoption threshold around 2018 and reaching <b>{mean_share:.1f}%</b> in 2025.
            </div>
            """, unsafe_allow_html=True)

    with c2:
        with st.container(border=True):
            st.markdown(f"""
            <div class="chart-meta-overline">METRIC #02 · MARKET LEADERSHIP</div>
            <div class="chart-title-text">2. Top 10 EV Adoption Leaders ({latest_yr})</div>
            <div class="chart-desc-text">Top economies ranked by electric vehicle market share of new sales in {latest_yr}</div>
            """, unsafe_allow_html=True)

            top10 = df_latest.sort_values("ev_market_share", ascending=False).head(10)
            fig_top10 = px.bar(
                top10, x="ev_market_share", y="country",
                orientation="h", color="ev_market_share",
                color_continuous_scale=["#93C5FD", "#2563EB", "#1D4ED8"],
                labels={"ev_market_share": "EV Share (%)", "country": "Country"},
                text_auto=".1f",
            )
            fig_top10.update_layout(**clean_plot_layout(height=300, show_legend=False))
            fig_top10.update_yaxes(autorange="reversed")
            fig_top10.update_coloraxes(showscale=False)
            fig_top10.update_traces(
                textposition="outside",
                hovertemplate="<b>Country:</b> %{y}<br>EV Share: <b>%{x:.1f}%</b><extra></extra>",
            )
            st.plotly_chart(fig_top10, use_container_width=True, config=PLOT_CONFIG)

            st.markdown(f"""
            <div class="chart-takeaway-box">
                <b>Analyst Finding:</b> <b>{top_nation['country']}</b> leads globally at <b>{top_nation['ev_market_share']:.1f}%</b>, driven by tax exemptions, followed by Sweden, Netherlands, and China.
            </div>
            """, unsafe_allow_html=True)

    # Row 2: Sales Mix & Cost Comparison
    c3, c4 = st.columns(2)

    with c3:
        with st.container(border=True):
            st.markdown(f"""
            <div class="chart-meta-overline">METRIC #03 · POWERTRAIN SPLIT</div>
            <div class="chart-title-text">3. Global New Car Sales Powertrain Mix ({latest_yr})</div>
            <div class="chart-desc-text">Aggregate breakdown of {latest_yr} vehicle registrations by fuel type</div>
            """, unsafe_allow_html=True)

            ev_tot = df_latest["ev_sales"].sum()
            petrol_tot = df_latest["petrol_car_sales"].sum()
            diesel_tot = df_latest["diesel_car_sales"].sum()
            grand_tot = ev_tot + petrol_tot + diesel_tot

            fig_donut = go.Figure(go.Pie(
                labels=["Petrol (Gasoline)", "Electric (EV)", "Diesel"],
                values=[petrol_tot, ev_tot, diesel_tot],
                hole=0.55,
                marker=dict(colors=[COLORS["petrol"], COLORS["ev"], COLORS["diesel"]]),
                textinfo="label+percent",
                hovertemplate="<b>Powertrain:</b> %{label}<br>Sales: %{value:,.0f} cars (%{percent})<extra></extra>",
            ))
            fig_donut.update_layout(**clean_plot_layout(height=300, show_legend=False))
            st.plotly_chart(fig_donut, use_container_width=True, config=PLOT_CONFIG)

            st.markdown(f"""
            <div class="chart-takeaway-box">
                <b>Analyst Finding:</b> Petrol remains the largest category ({petrol_tot/grand_tot*100:.0f}%), but EVs have captured nearly a quarter ({ev_tot/grand_tot*100:.0f}%) of new sales, rapidly displacing diesel vehicles.
            </div>
            """, unsafe_allow_html=True)

    with c4:
        with st.container(border=True):
            st.markdown("""
            <div class="chart-meta-overline">METRIC #04 · OPERATING ECONOMICS</div>
            <div class="chart-title-text">4. Fuel Cost per 100 km: Petrol vs. EV</div>
            <div class="chart-desc-text">Average energy cost to drive 100 km across surveyed nations (USD)</div>
            """, unsafe_allow_html=True)

            ice_c = df_latest["fuel_cost_100km"].mean()
            ev_c = df_latest["ev_cost_100km"].mean()
            savings_pct = ((ice_c - ev_c) / ice_c) * 100

            fig_cost = go.Figure(go.Bar(
                x=["Petrol Vehicle", "Electric Vehicle (EV)"],
                y=[ice_c, ev_c],
                marker=dict(color=[COLORS["petrol"], COLORS["green"]]),
                text=[f"${ice_c:.2f}", f"${ev_c:.2f}"],
                textposition="outside",
                hovertemplate="<b>Powertrain:</b> %{x}<br>Energy Cost: $%{y:.2f} per 100 km<extra></extra>",
            ))
            fig_cost.update_layout(**clean_plot_layout(height=300, show_legend=False))
            fig_cost.update_yaxes(title="Cost per 100 km (USD)", range=[0, max(ice_c, ev_c) * 1.25])
            st.plotly_chart(fig_cost, use_container_width=True, config=PLOT_CONFIG)

            st.markdown(f"""
            <div class="chart-takeaway-box">
                <b>Analyst Finding:</b> Driving an EV costs only <b>${ev_c:.2f}</b> per 100 km compared to <b>${ice_c:.2f}</b> for petrol — saving drivers ~<b>{savings_pct:.0f}% on fuel costs</b> (approx. $1,000/year over 15,000 km).
            </div>
            """, unsafe_allow_html=True)

    # Row 3: Infrastructure Buildout & Emissions Trajectory
    c5, c6 = st.columns(2)

    with c5:
        with st.container(border=True):
            st.markdown(f"""
            <div class="chart-meta-overline">METRIC #05 · CHARGING INFRASTRUCTURE</div>
            <div class="chart-title-text">5. Global Charging Infrastructure Buildout</div>
            <div class="chart-desc-text">Total public charging stations installed across the 25 countries ({earliest_yr}–{latest_yr})</div>
            """, unsafe_allow_html=True)

            infra_df = df.groupby("year", as_index=False)["charging_stations"].sum()
            fig_infra = px.bar(
                infra_df, x="year", y="charging_stations",
                color_discrete_sequence=[COLORS["primary"]],
                labels={"year": "Year", "charging_stations": "Public Chargers"},
            )
            fig_infra.update_traces(hovertemplate="<b>Year:</b> %{x}<br>Public Chargers: <b>%{y:,.0f}</b><extra></extra>")
            fig_infra.update_layout(**clean_plot_layout(height=300, show_legend=False))
            st.plotly_chart(fig_infra, use_container_width=True, config=PLOT_CONFIG)

            st.markdown(f"""
            <div class="chart-takeaway-box">
                <b>Analyst Finding:</b> Public charging installations expanded from <b>{fmt_val(infra_df.iloc[0]['charging_stations'])}</b> in 2010 to <b>{fmt_val(infra_df.iloc[-1]['charging_stations'])}</b> in {latest_yr}, resolving consumer range anxiety.
            </div>
            """, unsafe_allow_html=True)

    with c6:
        with st.container(border=True):
            st.markdown("""
            <div class="chart-meta-overline">METRIC #06 · DECARBONIZATION</div>
            <div class="chart-title-text">6. Transport Sector CO₂ Emissions Trajectory</div>
            <div class="chart-desc-text">Average road transport carbon emissions (Million tonnes CO₂)</div>
            """, unsafe_allow_html=True)

            em_df = df.groupby("year", as_index=False)["co2_emissions_transport_mt"].mean()
            fig_em = px.line(
                em_df, x="year", y="co2_emissions_transport_mt",
                markers=True, color_discrete_sequence=[COLORS["red"]],
                labels={"year": "Year", "co2_emissions_transport_mt": "Emissions (Mt CO₂)"},
            )
            fig_em.update_traces(hovertemplate="<b>Year:</b> %{x}<br>Transport Emissions: <b>%{y:.1f} Mt</b><extra></extra>")
            peak_row = em_df.loc[em_df["co2_emissions_transport_mt"].idxmax()]
            fig_em.add_annotation(
                x=peak_row["year"], y=peak_row["co2_emissions_transport_mt"],
                text=f"Peak: {peak_row['co2_emissions_transport_mt']:.1f} Mt",
                showarrow=True, arrowhead=2, yshift=12, font=dict(color=COLORS["red"], size=12),
            )
            fig_em.update_layout(**clean_plot_layout(height=300, show_legend=False))
            st.plotly_chart(fig_em, use_container_width=True, config=PLOT_CONFIG)

            st.markdown("""
            <div class="chart-takeaway-box">
                <b>Analyst Finding:</b> Transport emissions peaked and are beginning to bend downwards. Because internal combustion cars last 12–15 years, emissions decline gradually as old fleets are retired.
            </div>
            """, unsafe_allow_html=True)

    # Row 4: Battery Range & Fleet Substitution
    c7, c8 = st.columns(2)

    with c7:
        with st.container(border=True):
            st.markdown("""
            <div class="chart-meta-overline">METRIC #07 · BATTERY TECHNOLOGY</div>
            <div class="chart-title-text">7. Battery Range Progression (km on single charge)</div>
            <div class="chart-desc-text">Average driving range of electric vehicles sold each year</div>
            """, unsafe_allow_html=True)

            range_df = df.groupby("year", as_index=False)["avg_ev_range_km"].mean()
            fig_range = px.area(
                range_df, x="year", y="avg_ev_range_km",
                color_discrete_sequence=[COLORS["green"]],
                labels={"year": "Year", "avg_ev_range_km": "Battery Range (km)"},
            )
            fig_range.update_traces(hovertemplate="<b>Year:</b> %{x}<br>Average Range: <b>%{y:.0f} km</b><extra></extra>")
            fig_range.update_layout(**clean_plot_layout(height=300, show_legend=False))
            fig_range.update_yaxes(range=[0, 550])
            st.plotly_chart(fig_range, use_container_width=True, config=PLOT_CONFIG)

            st.markdown(f"""
            <div class="chart-takeaway-box">
                <b>Analyst Finding:</b> Average single-charge range quadrupled from <b>{range_df.iloc[0]['avg_ev_range_km']:.0f} km</b> in 2010 to <b>{range_df.iloc[-1]['avg_ev_range_km']:.0f} km</b> in 2025, matching conventional petrol vehicles.
            </div>
            """, unsafe_allow_html=True)

    with c8:
        with st.container(border=True):
            st.markdown(f"""
            <div class="chart-meta-overline">METRIC #08 · FLEET DISPLACEMENT</div>
            <div class="chart-title-text">8. Fleet Substitution: Annual Sales by Fuel Type</div>
            <div class="chart-desc-text">Total vehicles registered across the 25 economies ({earliest_yr}–{latest_yr})</div>
            """, unsafe_allow_html=True)

            fleet_trend = df.groupby("year", as_index=False).agg(
                ev=("ev_sales", "sum"),
                petrol=("petrol_car_sales", "sum"),
                diesel=("diesel_car_sales", "sum"),
            )
            fig_fleet = go.Figure()
            fig_fleet.add_trace(go.Scatter(
                x=fleet_trend["year"], y=fleet_trend["ev"], name="Electric",
                stackgroup="one", fill="tonexty", fillcolor="rgba(37,99,235,0.45)", line=dict(color=COLORS["ev"]),
                hovertemplate="<b>Year:</b> %{x}<br>EV Sales: <b>%{y:,.0f} units</b><extra></extra>",
            ))
            fig_fleet.add_trace(go.Scatter(
                x=fleet_trend["year"], y=fleet_trend["petrol"], name="Petrol",
                stackgroup="one", fill="tonexty", fillcolor="rgba(217,119,6,0.45)", line=dict(color=COLORS["petrol"]),
                hovertemplate="<b>Year:</b> %{x}<br>Petrol Sales: <b>%{y:,.0f} units</b><extra></extra>",
            ))
            fig_fleet.add_trace(go.Scatter(
                x=fleet_trend["year"], y=fleet_trend["diesel"], name="Diesel",
                stackgroup="one", fill="tonexty", fillcolor="rgba(100,116,139,0.45)", line=dict(color=COLORS["diesel"]),
                hovertemplate="<b>Year:</b> %{x}<br>Diesel Sales: <b>%{y:,.0f} units</b><extra></extra>",
            ))
            fig_fleet.update_layout(**clean_plot_layout(height=300))
            st.plotly_chart(fig_fleet, use_container_width=True, config=PLOT_CONFIG)

            st.markdown("""
            <div class="chart-takeaway-box">
                <b>Analyst Finding:</b> The stacked volume shows electric vehicles steadily expanding their share of total vehicle production, capturing market share primarily from retiring diesel platforms.
            </div>
            """, unsafe_allow_html=True)

    # Row 5: Policy Effectiveness & Energy Economics
    c9, c10 = st.columns(2)

    with c9:
        with st.container(border=True):
            st.markdown(f"""
            <div class="chart-meta-overline">METRIC #09 · POLICY EFFICACY</div>
            <div class="chart-title-text">9. Incentive Effectiveness: Subsidies vs. EV Market Share ({latest_yr})</div>
            <div class="chart-desc-text">Direct relationship between government purchase subsidies and resulting EV penetration</div>
            """, unsafe_allow_html=True)

            fig_sub = px.scatter(
                df_latest, x="ev_subsidy_usd", y="ev_market_share",
                color="region", size="ev_sales", hover_name="country",
                color_discrete_sequence=CHART_PALETTE,
                labels={"ev_subsidy_usd": "Government Subsidy ($/EV)", "ev_market_share": "EV Market Share (%)"},
            )
            fig_sub.update_traces(
                marker=dict(line=dict(width=1.5, color="#FFFFFF")),
                hovertemplate="<b>Country:</b> %{hovertext}<br>Subsidy: $%{x:,.0f}<br>EV Share: <b>%{y:.1f}%</b><br>Sales: %{marker.size:,.0f} units<extra></extra>",
            )
            fig_sub.update_layout(**clean_plot_layout(height=300))
            st.plotly_chart(fig_sub, use_container_width=True, config=PLOT_CONFIG)

            st.markdown("""
            <div class="chart-takeaway-box">
                <b>Analyst Finding:</b> Nations offering purchase subsidies over <b>$4,000</b> achieved rapid consumer adoption. Once market share crossed 20%, organic network effects maintain growth.
            </div>
            """, unsafe_allow_html=True)

    with c10:
        with st.container(border=True):
            st.markdown(f"""
            <div class="chart-meta-overline">METRIC #10 · ENERGY SPREAD</div>
            <div class="chart-title-text">10. Global Energy Price Disparity: Petrol vs. Electricity ({latest_yr})</div>
            <div class="chart-desc-text">Average fuel price ($/Litre) vs. electricity rate ($/kWh) by geographic region</div>
            """, unsafe_allow_html=True)

            energy_reg = df_latest[df_latest["region"].isin(["Europe", "Asia-Pacific", "Americas"])].groupby("region", as_index=False).agg(
                petrol=("fuel_price_usd_per_liter", "mean"),
                elec=("electricity_price_usd_per_kwh", "mean"),
            )
            fig_en = go.Figure()
            fig_en.add_trace(go.Bar(
                name="Petrol ($/Litre)", x=energy_reg["region"], y=energy_reg["petrol"],
                marker_color=COLORS["petrol"], text=energy_reg["petrol"].apply(lambda x: f"${x:.2f}"),
                textposition="outside", hovertemplate="<b>Region:</b> %{x}<br>Petrol: <b>$%{y:.2f} / L</b><extra></extra>",
            ))
            fig_en.add_trace(go.Bar(
                name="Electricity ($/kWh)", x=energy_reg["region"], y=energy_reg["elec"],
                marker_color=COLORS["primary"], text=energy_reg["elec"].apply(lambda x: f"${x:.2f}"),
                textposition="outside", hovertemplate="<b>Region:</b> %{x}<br>Electricity: <b>$%{y:.2f} / kWh</b><extra></extra>",
            ))
            fig_en.update_layout(**clean_plot_layout(height=300), barmode="group")
            st.plotly_chart(fig_en, use_container_width=True, config=PLOT_CONFIG)

            st.markdown("""
            <div class="chart-takeaway-box">
                <b>Analyst Finding:</b> European petrol costs (~$1.85/L) make EV economics overwhelmingly favorable, while low domestic electricity rates in the Americas provide strong annual per-driver cost savings.
            </div>
            """, unsafe_allow_html=True)

    # Row 6: Regulatory Stringency & Charging Density
    c11, c12 = st.columns(2)

    with c11:
        with st.container(border=True):
            st.markdown("""
            <div class="chart-meta-overline">METRIC #11 · REGULATORY STRINGENCY</div>
            <div class="chart-title-text">11. Vehicle Emission Standards Tightening (2010–2025)</div>
            <div class="chart-desc-text">Average vehicle emission regulation stringency score (0 = no policy, 100 = aggressive mandate)</div>
            """, unsafe_allow_html=True)

            reg_trend = df.groupby("year", as_index=False)["emission_regulation_score"].mean()
            fig_reg = px.line(
                reg_trend, x="year", y="emission_regulation_score",
                markers=True, color_discrete_sequence=[COLORS["purple"]],
                labels={"year": "Year", "emission_regulation_score": "Policy Score (0–100)"},
            )
            fig_reg.update_traces(
                line=dict(width=3), marker=dict(size=7),
                hovertemplate="<b>Year:</b> %{x}<br>Regulation Stringency: <b>%{y:.1f} / 100</b><extra></extra>",
            )
            fig_reg.update_layout(**clean_plot_layout(height=300, show_legend=False))
            fig_reg.update_yaxes(range=[30, 95])
            st.plotly_chart(fig_reg, use_container_width=True, config=PLOT_CONFIG)

            st.markdown("""
            <div class="chart-takeaway-box">
                <b>Analyst Finding:</b> Global policy scores rose from <b>44 in 2010 to 83 in 2025</b>. Fleet penalties and ICE ban targets forced legacy automakers to pivot capital expenditures to electric platforms.
            </div>
            """, unsafe_allow_html=True)

    with c12:
        with st.container(border=True):
            st.markdown(f"""
            <div class="chart-meta-overline">METRIC #12 · GRID READINESS</div>
            <div class="chart-title-text">12. Public Charging Density: Chargers per 1,000 EVs ({latest_yr})</div>
            <div class="chart-desc-text">Top markets ranked by public chargers available per 1,000 electric vehicles on the road</div>
            """, unsafe_allow_html=True)

            top_dens = df_latest.sort_values("chargers_per_1k_ev", ascending=False).head(10)
            fig_dens = px.bar(
                top_dens, x="country", y="chargers_per_1k_ev",
                color="country", color_discrete_sequence=CHART_PALETTE,
                text_auto=".0f", labels={"country": "Country", "chargers_per_1k_ev": "Chargers / 1k EVs"},
            )
            fig_dens.update_traces(
                textposition="outside",
                hovertemplate="<b>Country:</b> %{x}<br>Chargers per 1,000 EVs: <b>%{y:.0f}</b><extra></extra>",
            )
            fig_dens.update_layout(**clean_plot_layout(height=300, show_legend=False))
            fig_dens.update_yaxes(range=[0, top_dens["chargers_per_1k_ev"].max() * 1.25])
            st.plotly_chart(fig_dens, use_container_width=True, config=PLOT_CONFIG)

            st.markdown("""
            <div class="chart-takeaway-box">
                <b>Analyst Finding:</b> High charger density ensures low queuing times at fast-charging hubs, which directly correlates with higher consumer satisfaction and repeat EV purchases.
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2: 🛠️ CUSTOM CHART STUDIO (GRAPH GENERATOR & EXPLICIT TOOLTIPS)
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🛠️ Custom Chart Studio":
    st.markdown("""
    <div class="page-header-container">
        <div class="page-eyebrow">STUDIO / VISUALIZATION ENGINE</div>
        <div class="page-title">Interactive Chart Studio</div>
        <div class="page-desc">Generate customized, presentation-ready visualizations by selecting compatible variables, time windows, and chart formats.</div>
    </div>
    """, unsafe_allow_html=True)

    # Initialize render version counter to allow resetting ONLY the graph display without touching dropdown options
    if "studio_graph_render_id" not in st.session_state:
        st.session_state["studio_graph_render_id"] = 0

    # Preset Callbacks
    def apply_studio_preset(c_format, x_col, y_col, color_col, yr_scope):
        st.session_state["studio_c_type"] = c_format
        st.session_state["studio_x"] = x_col
        st.session_state["studio_y"] = y_col
        st.session_state["studio_color"] = color_col
        st.session_state["studio_time_mode"] = yr_scope
        st.session_state["studio_graph_render_id"] += 1

    def reset_displayed_graph_only():
        """Resets ONLY the displayed graph view to pristine autoscale without wiping dropdown choices."""
        st.session_state["studio_graph_render_id"] += 1

    def reset_all_studio():
        """Full reset back to default Bar Chart."""
        st.session_state["studio_c_type"] = "Bar Chart"
        st.session_state["studio_x"] = "country"
        st.session_state["studio_y"] = "ev_market_share"
        st.session_state["studio_color"] = "region"
        st.session_state["studio_time_mode"] = "Latest Year Only (2025)"
        st.session_state["studio_year_slider"] = (earliest_yr, latest_yr)
        st.session_state["studio_graph_render_id"] += 1

    # 1-Click Templates Row
    st.markdown('<div class="chart-meta-overline" style="margin-bottom: 0.4rem;">QUICK TEMPLATES & VIEW ACTIONS</div>', unsafe_allow_html=True)
    t_c1, t_c2, t_c3, t_c4, t_c5, t_c6 = st.columns([1, 1, 1, 1, 1.25, 1])
    with t_c1:
        st.button("🔌 Chargers vs. Share", on_click=apply_studio_preset, args=("Scatter Plot", "charging_stations", "ev_market_share", "region", "Latest Year Only (2025)"), use_container_width=True)
    with t_c2:
        st.button("📈 Adoption Over Time", on_click=apply_studio_preset, args=("Line Chart", "year", "ev_market_share", "region", "Custom Year Range"), use_container_width=True)
    with t_c3:
        st.button("🚗 Sales by Country", on_click=apply_studio_preset, args=("Bar Chart", "country", "ev_sales", "region", "Latest Year Only (2025)"), use_container_width=True)
    with t_c4:
        st.button("🔋 Battery Range Jump", on_click=apply_studio_preset, args=("Area Chart", "year", "avg_ev_range_km", "None", "Custom Year Range"), use_container_width=True)
    with t_c5:
        st.button("🔄 Reset Graph View", on_click=reset_displayed_graph_only, use_container_width=True, help="Refreshes and unzooms ONLY the active graph back to full autoscale, keeping your selected variables intact.")
    with t_c6:
        st.button("⚠️ Reset All", on_click=reset_all_studio, use_container_width=True, help="Reset studio options back to initial defaults")

    st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)

    # Variable Classification for Smart Compatibility
    CATEGORICAL_X = ["country", "region"]
    TEMPORAL_X = ["year"]
    NUMERICAL_METRICS = [
        "ev_market_share", "ev_sales", "petrol_car_sales", "diesel_car_sales",
        "total_vehicle_sales", "charging_stations", "avg_ev_range_km",
        "fuel_price_usd_per_liter", "electricity_price_usd_per_kwh",
        "co2_emissions_transport_mt", "ev_subsidy_usd", "emission_regulation_score",
        "fuel_cost_100km", "ev_cost_100km", "savings_100km",
    ]
    ALL_X_OPTIONS = ["country", "region", "year"] + NUMERICAL_METRICS

    # Initialize studio session state keys safely
    if "studio_c_type" not in st.session_state:
        st.session_state["studio_c_type"] = "Bar Chart"
    if "studio_x" not in st.session_state:
        st.session_state["studio_x"] = "country"
    if "studio_y" not in st.session_state:
        st.session_state["studio_y"] = "ev_market_share"
    if "studio_color" not in st.session_state:
        st.session_state["studio_color"] = "region"
    if "studio_time_mode" not in st.session_state:
        st.session_state["studio_time_mode"] = "Latest Year Only (2025)"
    if "studio_year_slider" not in st.session_state:
        st.session_state["studio_year_slider"] = (earliest_yr, latest_yr)

    # Studio Controls inside native bordered container (zero unclosed HTML tags)
    with st.container(border=True):
        st.markdown('<div class="chart-meta-overline">STEP 01 / HORIZONTAL AXIS CONFIGURATION</div>', unsafe_allow_html=True)
        col_x1, col_x2 = st.columns([1, 1])

        with col_x1:
            curr_x = st.selectbox(
                "Horizontal Axis (X)",
                options=ALL_X_OPTIONS,
                format_func=label_of,
                key="studio_x",
            )

        # Smart dynamic filtering of Y-axis and Chart formats based on X
        if curr_x in CATEGORICAL_X:
            valid_y_options = NUMERICAL_METRICS
            valid_formats = ["Bar Chart", "Donut Chart", "Scatter Plot"]
        elif curr_x in TEMPORAL_X:
            valid_y_options = NUMERICAL_METRICS
            valid_formats = ["Line Chart", "Area Chart", "Bar Chart"]
        else:
            # Numeric X: Compare against other numerical metrics
            valid_y_options = [c for c in NUMERICAL_METRICS if c != curr_x]
            valid_formats = ["Scatter Plot", "Bar Chart", "Line Chart"]

        # Ensure current selections are valid for newly selected X
        if st.session_state["studio_y"] not in valid_y_options:
            st.session_state["studio_y"] = valid_y_options[0]
        if st.session_state["studio_c_type"] not in valid_formats:
            st.session_state["studio_c_type"] = valid_formats[0]

        with col_x2:
            y_metric = st.selectbox(
                "Vertical Metric (Y)",
                options=valid_y_options,
                format_func=label_of,
                key="studio_y",
            )

        st.markdown('<div class="chart-meta-overline" style="margin-top: 0.8rem;">STEP 02 / CHART FORMAT & VISUAL STRATIFICATION</div>', unsafe_allow_html=True)
        col_m1, col_m2 = st.columns([1, 1])

        with col_m1:
            c_format = st.selectbox(
                "Chart Format",
                options=valid_formats,
                key="studio_c_type",
            )

        with col_m2:
            # When region is chosen as X, only allow None or region to strictly preserve 3 regions
            if curr_x == "region":
                color_choices = ["None", "region"]
            else:
                color_choices = ["None", "region", "country"]

            if st.session_state.get("studio_color") not in color_choices:
                st.session_state["studio_color"] = color_choices[0]

            color_choice = st.selectbox(
                "Color Stratification",
                options=color_choices,
                format_func=lambda x: "Single Unified Tone" if x=="None" else label_of(x),
                key="studio_color",
            )

        # Step 3: Time Selection
        st.markdown('<div class="chart-meta-overline" style="margin-top: 0.8rem;">STEP 03 / TEMPORAL WINDOW & HORIZON</div>', unsafe_allow_html=True)
        f_c1, f_c2 = st.columns([1, 2])

        with f_c1:
            time_mode = st.radio(
                "Time Window Scope",
                options=["Latest Year Only (2025)", "Custom Year Range"],
                horizontal=True,
                key="studio_time_mode",
            )
        with f_c2:
            if time_mode == "Custom Year Range":
                studio_years = st.slider(
                    "Year Range Slider",
                    min_value=earliest_yr,
                    max_value=latest_yr,
                    key="studio_year_slider",
                )
            else:
                studio_years = (latest_yr, latest_yr)
                st.caption(f"Viewing snapshot data for {latest_yr} only.")

    # Data slice for studio - filter to 3 canonical regions
    s_df = df[
        (df["year"].between(studio_years[0], studio_years[1])) &
        (df["region"].isin(["Europe", "Asia-Pacific", "Americas"]))
    ].dropna(subset=[curr_x, y_metric]).copy()

    # Bulletproof Chart Generation with Fallback Guard & Explicit Tooltip Prefixes
    fig_studio = None
    chart_error = None

    try:
        if s_df.empty:
            chart_error = "No data points available for the chosen time range."
        elif c_format == "Bar Chart":
            if curr_x == "region":
                # STRICTLY ONLY 3 REGIONS
                agg_data = s_df.groupby("region", as_index=False)[y_metric].mean()
                agg_data = agg_data[agg_data["region"].isin(["Europe", "Asia-Pacific", "Americas"])]
                fig_studio = px.bar(
                    agg_data, x="region", y=y_metric,
                    color="region" if color_choice == "region" else None,
                    color_discrete_sequence=[COLORS["primary"], COLORS["green"], COLORS["petrol"]],
                    text_auto=".1f" if agg_data[y_metric].max() < 1000 else False,
                    labels={"region": "Region", y_metric: label_of(y_metric)},
                )
                fig_studio.update_traces(
                    textposition="outside",
                    hovertemplate="<b>Region:</b> %{x}<br>" + label_of(y_metric) + ": <b>%{y:,.1f}</b><extra></extra>",
                )
            elif curr_x == "country":
                grp_cols = ["country"] + ([color_choice] if color_choice not in ["None", "country"] else [])
                agg_data = s_df.groupby(grp_cols, as_index=False)[y_metric].mean()
                agg_data = agg_data.sort_values(y_metric, ascending=False).head(25)
                fig_studio = px.bar(
                    agg_data, x="country", y=y_metric,
                    color=None if color_choice=="None" else color_choice,
                    color_discrete_sequence=CHART_PALETTE,
                    text_auto=".1f" if agg_data[y_metric].max() < 1000 else False,
                    labels={"country": "Country", y_metric: label_of(y_metric)},
                )
                if color_choice == "region":
                    fig_studio.update_traces(
                        textposition="outside",
                        hovertemplate="<b>Country:</b> %{x}<br><b>Region:</b> %{data.name}<br>" + label_of(y_metric) + ": <b>%{y:,.1f}</b><extra></extra>",
                    )
                else:
                    fig_studio.update_traces(
                        textposition="outside",
                        hovertemplate="<b>Country:</b> %{x}<br>" + label_of(y_metric) + ": <b>%{y:,.1f}</b><extra></extra>",
                    )
            else:
                grp_cols = [curr_x] + ([color_choice] if color_choice != "None" else [])
                agg_data = s_df.groupby(grp_cols, as_index=False)[y_metric].mean()
                fig_studio = px.bar(
                    agg_data, x=curr_x, y=y_metric,
                    color=None if color_choice=="None" else color_choice,
                    color_discrete_sequence=CHART_PALETTE,
                    labels={curr_x: label_of(curr_x), y_metric: label_of(y_metric)},
                )
                prefix_x = "Year" if curr_x=="year" else label_of(curr_x)
                fig_studio.update_traces(
                    hovertemplate=f"<b>{prefix_x}:</b> %{{x}}<br>" + label_of(y_metric) + ": <b>%{y:,.1f}</b><extra></extra>",
                )

        elif c_format == "Line Chart":
            if curr_x == "year" and color_choice != "None":
                line_data = s_df.groupby(["year", color_choice], as_index=False)[y_metric].mean()
                fig_studio = px.line(
                    line_data, x="year", y=y_metric, color=color_choice, markers=True,
                    color_discrete_sequence=CHART_PALETTE,
                    labels={"year": "Year", y_metric: label_of(y_metric)},
                )
                prefix_c = "Region" if color_choice == "region" else "Country"
                fig_studio.update_traces(
                    marker=dict(size=7),
                    hovertemplate=f"<b>Year:</b> %{{x}}<br><b>{prefix_c}:</b> %{{data.name}}<br>" + label_of(y_metric) + ": <b>%{y:,.1f}</b><extra></extra>",
                )
            else:
                line_data = s_df.groupby(curr_x, as_index=False)[y_metric].mean()
                fig_studio = px.line(
                    line_data, x=curr_x, y=y_metric, markers=True,
                    color_discrete_sequence=[COLORS["primary"]],
                    labels={curr_x: label_of(curr_x), y_metric: label_of(y_metric)},
                )
                prefix_x = "Year" if curr_x=="year" else ("Region" if curr_x=="region" else ("Country" if curr_x=="country" else label_of(curr_x)))
                fig_studio.update_traces(
                    marker=dict(size=7),
                    hovertemplate=f"<b>{prefix_x}:</b> %{{x}}<br>" + label_of(y_metric) + ": <b>%{y:,.1f}</b><extra></extra>",
                )

        elif c_format == "Scatter Plot":
            fig_studio = px.scatter(
                s_df, x=curr_x, y=y_metric,
                color=None if color_choice=="None" else color_choice,
                hover_name="country",
                color_discrete_sequence=CHART_PALETTE,
                labels={curr_x: label_of(curr_x), y_metric: label_of(y_metric)},
                trendline="ols" if pd.api.types.is_numeric_dtype(s_df[curr_x]) and len(s_df)>5 else None,
            )
            fig_studio.update_traces(
                marker=dict(size=9, line=dict(width=1.5, color="#FFFFFF")),
                hovertemplate="<b>Country:</b> %{hovertext}<br>" + label_of(curr_x) + ": %{x:,.1f}<br>" + label_of(y_metric) + ": <b>%{y:,.1f}</b><extra></extra>",
            )
            if pd.api.types.is_numeric_dtype(s_df[curr_x]) and s_df[curr_x].max() > 1000:
                fig_studio.update_xaxes(type="log")

        elif c_format == "Area Chart":
            area_data = s_df.groupby(curr_x, as_index=False)[y_metric].mean()
            fig_studio = px.area(
                area_data, x=curr_x, y=y_metric,
                color_discrete_sequence=[COLORS["primary"]],
                labels={curr_x: label_of(curr_x), y_metric: label_of(y_metric)},
            )
            prefix_x = "Year" if curr_x=="year" else ("Region" if curr_x=="region" else ("Country" if curr_x=="country" else label_of(curr_x)))
            fig_studio.update_traces(
                hovertemplate=f"<b>{prefix_x}:</b> %{{x}}<br>" + label_of(y_metric) + ": <b>%{y:,.1f}</b><extra></extra>",
            )

        elif c_format == "Donut Chart":
            d_group = curr_x if curr_x in ["country", "region"] else "region"
            pie_data = s_df.groupby(d_group, as_index=False)[y_metric].sum()
            if d_group == "region":
                pie_data = pie_data[pie_data["region"].isin(["Europe", "Asia-Pacific", "Americas"])]
                prefix_d = "Region"
            else:
                prefix_d = "Country"

            fig_studio = go.Figure(go.Pie(
                labels=pie_data[d_group],
                values=pie_data[y_metric],
                hole=0.55,
                marker=dict(colors=CHART_PALETTE),
                textinfo="label+percent",
                hovertemplate=f"<b>{prefix_d}:</b> %{{label}}<br>" + label_of(y_metric) + ": <b>%{value:,.0f}</b> (%{percent})<extra></extra>",
            ))

    except Exception as e:
        chart_error = f"This chart combination is currently not supported for this slice of data. ({str(e)})"

    if chart_error:
        st.info(f"ℹ️ {chart_error} Please adjust your X and Y selections, or click **⚠️ Reset All** above.")
    elif fig_studio:
        with st.container(border=True):
            hdr_c1, hdr_c2 = st.columns([3, 1])
            with hdr_c1:
                st.markdown(f'<div class="chart-meta-overline">GENERATED VISUALIZATION · {c_format.upper()}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="chart-title-text">{label_of(y_metric)} by {label_of(curr_x)}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="chart-desc-text">Temporal Scope: {studio_years[0]}–{studio_years[1]} · Sample Size: {len(s_df):,} Data Points</div>', unsafe_allow_html=True)
            with hdr_c2:
                st.caption("Double-click graph anytime to reset zoom")

            fig_studio.update_layout(**clean_plot_layout(height=400, show_legend=(color_choice != "None")))
            st.plotly_chart(
                fig_studio,
                use_container_width=True,
                key=f"studio_plot_view_{st.session_state['studio_graph_render_id']}",
                config=PLOT_CONFIG,
            )

        # Summary Metrics Row
        s1, s2, s3, s4 = st.columns(4)
        with s1:
            st.markdown(f"""
            <div class="kpi-card accent-blue">
                <div class="kpi-label">Cohort Average</div>
                <div class="kpi-value">{s_df[y_metric].mean():,.1f}</div>
                <div class="kpi-subtext">Mean of selected slice</div>
            </div>
            """, unsafe_allow_html=True)
        with s2:
            max_idx = s_df[y_metric].idxmax()
            st.markdown(f"""
            <div class="kpi-card accent-emerald">
                <div class="kpi-label">Highest Recorded</div>
                <div class="kpi-value">{s_df.loc[max_idx, y_metric]:,.1f}</div>
                <div class="kpi-delta-pill">{s_df.loc[max_idx, 'country']}</div>
            </div>
            """, unsafe_allow_html=True)
        with s3:
            min_idx = s_df[y_metric].idxmin()
            st.markdown(f"""
            <div class="kpi-card accent-amber">
                <div class="kpi-label">Lowest Recorded</div>
                <div class="kpi-value">{s_df.loc[min_idx, y_metric]:,.1f}</div>
                <div class="kpi-delta-pill" style="background:#FFFBEB; color:#D97706; border-color:#FDE68A;">{s_df.loc[min_idx, 'country']}</div>
            </div>
            """, unsafe_allow_html=True)
        with s4:
            if pd.api.types.is_numeric_dtype(s_df[curr_x]) and curr_x != y_metric:
                corr_v = s_df[curr_x].corr(s_df[y_metric])
                st.markdown(f"""
                <div class="kpi-card accent-indigo">
                    <div class="kpi-label">Correlation (r)</div>
                    <div class="kpi-value">{corr_v:.2f}</div>
                    <div class="kpi-subtext">Pearson correlation coeff</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="kpi-card accent-indigo">
                    <div class="kpi-label">Data Points</div>
                    <div class="kpi-value">{len(s_df):,}</div>
                    <div class="kpi-subtext">Plotted observations</div>
                </div>
                """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3: 👥 COUNTRY & REGIONAL COMPARISONS (MATCHING 12 HIGH-VALUE GRAPHS)
# ══════════════════════════════════════════════════════════════════════════════
elif page == "👥 Country Comparisons":
    st.markdown("""
    <div class="page-header-container">
        <div class="page-eyebrow">BENCHMARKING / CROSS-MARKET COMPARISON</div>
        <div class="page-title">Country & Regional Benchmarking</div>
        <div class="page-desc">Compare sovereign markets head-to-head across adoption velocity, scale, and policy, or analyze broader regional macroeconomic trends across identical key metrics.</div>
    </div>
    """, unsafe_allow_html=True)

    tab_country, tab_region = st.tabs(["👥 Sovereign Country Comparisons", "🌐 Regional Comparison (Europe vs. Asia-Pacific vs. Americas)"])

    # ── TAB 1: SOVEREIGN COUNTRY COMPARISONS (12 HIGH-VALUE GRAPHS) ──
    with tab_country:
        with st.container(border=True):
            c_pick1, c_pick2 = st.columns([3, 1])
            with c_pick1:
                selected_benchmarks = st.multiselect(
                    "Select Sovereign Countries to Compare",
                    options=all_countries,
                    default=["Norway", "Germany", "United States", "China", "India", "France"],
                    help="Select any 2 to 8 countries to compare",
                    key="cmp_country_picker",
                )
            with c_pick2:
                bench_year = st.selectbox(
                    "Observation Year",
                    options=sorted(all_years, reverse=True),
                    index=0,
                    key="cmp_year_picker",
                )

        if not selected_benchmarks:
            selected_benchmarks = ["Norway", "Germany", "United States", "China"]

        cmp_df = df[(df["country"].isin(selected_benchmarks)) & (df["year"] == bench_year)].sort_values("ev_market_share", ascending=False)

        # Row 1: EV Market Share vs Sales Volume
        g_c1, g_c2 = st.columns(2)
        with g_c1:
            with st.container(border=True):
                st.markdown(f"""
                <div class="chart-meta-overline">BENCHMARK #01 · PENETRATION</div>
                <div class="chart-title-text">1. EV Market Share (% of car sales in {bench_year})</div>
                <div class="chart-desc-text">Percentage of all newly sold vehicles that are electric</div>
                """, unsafe_allow_html=True)

                fig_g1 = px.bar(
                    cmp_df, x="country", y="ev_market_share",
                    color="country", color_discrete_sequence=CHART_PALETTE,
                    text_auto=".1f", labels={"country": "Country", "ev_market_share": "EV Share (%)"},
                )
                fig_g1.update_traces(
                    textposition="outside",
                    hovertemplate="<b>Country:</b> %{x}<br>EV Share: <b>%{y:.1f}%</b><extra></extra>",
                )
                fig_g1.update_layout(**clean_plot_layout(height=300, show_legend=False))
                fig_g1.update_yaxes(range=[0, cmp_df["ev_market_share"].max() * 1.25])
                st.plotly_chart(fig_g1, use_container_width=True, config=PLOT_CONFIG)

                st.markdown("""
                <div class="chart-takeaway-box">
                    <b>Analyst Finding:</b> Shows consumer adoption velocity. Smaller pioneering economies often lead in share due to focused subsidies.
                </div>
                """, unsafe_allow_html=True)

        with g_c2:
            with st.container(border=True):
                st.markdown(f"""
                <div class="chart-meta-overline">BENCHMARK #02 · SCALE</div>
                <div class="chart-title-text">2. Total EV Sales Volume (Vehicles sold in {bench_year})</div>
                <div class="chart-desc-text">Physical volume of electric cars registered</div>
                """, unsafe_allow_html=True)

                fig_g2 = px.bar(
                    cmp_df, x="country", y="ev_sales",
                    color="country", color_discrete_sequence=CHART_PALETTE,
                    labels={"country": "Country", "ev_sales": "Annual EV Sales"},
                )
                fig_g2.update_traces(
                    hovertemplate="<b>Country:</b> %{x}<br>EV Sales Volume: <b>%{y:,.0f} units</b><extra></extra>",
                )
                fig_g2.update_layout(**clean_plot_layout(height=300, show_legend=False))
                st.plotly_chart(fig_g2, use_container_width=True, config=PLOT_CONFIG)

                st.markdown("""
                <div class="chart-takeaway-box">
                    <b>Analyst Finding:</b> Highlights absolute manufacturing and consumption scale. Large automotive markets drive global component volume.
                </div>
                """, unsafe_allow_html=True)

        # Row 2: Charging Infrastructure & Subsidies
        g_c3, g_c4 = st.columns(2)
        with g_c3:
            with st.container(border=True):
                st.markdown(f"""
                <div class="chart-meta-overline">BENCHMARK #03 · INFRASTRUCTURE</div>
                <div class="chart-title-text">3. Public Charging Stations Count ({bench_year})</div>
                <div class="chart-desc-text">Installed public charging stations ready for drivers</div>
                """, unsafe_allow_html=True)

                fig_g3 = px.bar(
                    cmp_df, x="country", y="charging_stations",
                    color="country", color_discrete_sequence=CHART_PALETTE,
                    labels={"country": "Country", "charging_stations": "Public Chargers"},
                )
                fig_g3.update_traces(
                    hovertemplate="<b>Country:</b> %{x}<br>Public Chargers: <b>%{y:,.0f}</b><extra></extra>",
                )
                fig_g3.update_layout(**clean_plot_layout(height=300, show_legend=False))
                st.plotly_chart(fig_g3, use_container_width=True, config=PLOT_CONFIG)

                st.markdown("""
                <div class="chart-takeaway-box">
                    <b>Analyst Finding:</b> Countries that build extensive public charging infrastructure see significantly higher EV purchases.
                </div>
                """, unsafe_allow_html=True)

        with g_c4:
            with st.container(border=True):
                st.markdown(f"""
                <div class="chart-meta-overline">BENCHMARK #04 · FISCAL INCENTIVES</div>
                <div class="chart-title-text">4. Government EV Purchase Subsidy ($ in {bench_year})</div>
                <div class="chart-desc-text">Direct government financial incentive per vehicle purchase (USD)</div>
                """, unsafe_allow_html=True)

                fig_g4 = px.bar(
                    cmp_df, x="country", y="ev_subsidy_usd",
                    color="country", color_discrete_sequence=CHART_PALETTE,
                    text_auto="$,.0f", labels={"country": "Country", "ev_subsidy_usd": "Subsidy ($)"},
                )
                fig_g4.update_traces(
                    textposition="outside",
                    hovertemplate="<b>Country:</b> %{x}<br>Subsidy: <b>$%{y:,.0f}</b><extra></extra>",
                )
                fig_g4.update_layout(**clean_plot_layout(height=300, show_legend=False))
                fig_g4.update_yaxes(range=[0, max(cmp_df["ev_subsidy_usd"].max() * 1.25, 1000)])
                st.plotly_chart(fig_g4, use_container_width=True, config=PLOT_CONFIG)

                st.markdown("""
                <div class="chart-takeaway-box">
                    <b>Analyst Finding:</b> Direct consumer subsidies accelerate early adoption, after which cost parity maintains momentum.
                </div>
                """, unsafe_allow_html=True)

        # Row 3: 10-Year Progress Leap & Powertrain Fleet Mix
        g_c5, g_c6 = st.columns(2)
        with g_c5:
            with st.container(border=True):
                st.markdown("""
                <div class="chart-meta-overline">BENCHMARK #05 · DECADE LEAP</div>
                <div class="chart-title-text">5. 10-Year Leap: EV Share in 2015 vs. 2025</div>
                <div class="chart-desc-text">Direct grouped comparison showing decade adoption jumps</div>
                """, unsafe_allow_html=True)

                leap_df = df[(df["country"].isin(selected_benchmarks)) & (df["year"].isin([2015, 2025]))][["country", "year", "ev_market_share"]].copy()
                leap_df["year"] = leap_df["year"].astype(str)

                fig_leap = px.bar(
                    leap_df, x="country", y="ev_market_share", color="year",
                    barmode="group", color_discrete_map={"2015": "#94A3B8", "2025": COLORS["ev"]},
                    text_auto=".1f", labels={"country": "Country", "ev_market_share": "EV Share (%)", "year": "Year"},
                )
                fig_leap.update_traces(
                    textposition="outside",
                    hovertemplate="<b>Country:</b> %{x} (%{data.name})<br>EV Share: <b>%{y:.1f}%</b><extra></extra>",
                )
                fig_leap.update_layout(**clean_plot_layout(height=300))
                st.plotly_chart(fig_leap, use_container_width=True, config=PLOT_CONFIG)

                st.markdown("""
                <div class="chart-takeaway-box">
                    <b>Analyst Finding:</b> Highlights how rapidly the market transitioned from under 2% in 2015 to mass market penetration in 2025.
                </div>
                """, unsafe_allow_html=True)

        with g_c6:
            with st.container(border=True):
                st.markdown(f"""
                <div class="chart-meta-overline">BENCHMARK #06 · POWERTRAIN RATIO</div>
                <div class="chart-title-text">6. Powertrain Composition ({bench_year})</div>
                <div class="chart-desc-text">Vehicle sales split by Electric, Petrol, and Diesel</div>
                """, unsafe_allow_html=True)

                mix_df = df[(df["country"].isin(selected_benchmarks)) & (df["year"] == bench_year)][
                    ["country", "ev_sales", "petrol_car_sales", "diesel_car_sales"]
                ].copy()

                fig_mix = go.Figure()
                fig_mix.add_trace(go.Bar(name="EV", x=mix_df["country"], y=mix_df["ev_sales"], marker_color=COLORS["ev"]))
                fig_mix.add_trace(go.Bar(name="Petrol", x=mix_df["country"], y=mix_df["petrol_car_sales"], marker_color=COLORS["petrol"]))
                fig_mix.add_trace(go.Bar(name="Diesel", x=mix_df["country"], y=mix_df["diesel_car_sales"], marker_color=COLORS["diesel"]))
                fig_mix.update_layout(**clean_plot_layout(height=300), barmode="stack", yaxis_title="Vehicles Sold")
                fig_mix.update_traces(hovertemplate="<b>Country:</b> %{x}<br><b>%{data.name}:</b> %{y:,.0f} units<extra></extra>")
                st.plotly_chart(fig_mix, use_container_width=True, config=PLOT_CONFIG)

                st.markdown("""
                <div class="chart-takeaway-box">
                    <b>Analyst Finding:</b> Displays how each market balances traditional internal combustion fuels against growing EV sales.
                </div>
                """, unsafe_allow_html=True)

        # Row 4: Annual Driver Fuel Savings & Charger Density
        g_c7, g_c8 = st.columns(2)
        with g_c7:
            with st.container(border=True):
                st.markdown(f"""
                <div class="chart-meta-overline">BENCHMARK #07 · DRIVER ECONOMICS</div>
                <div class="chart-title-text">7. Annual Driver Fuel Cost Savings ($/year in {bench_year})</div>
                <div class="chart-desc-text">Estimated money saved annually by an EV driver (assuming 15,000 km driven)</div>
                """, unsafe_allow_html=True)

                fig_g7 = px.bar(
                    cmp_df, x="country", y="annual_savings",
                    color="country", color_discrete_sequence=CHART_PALETTE,
                    text_auto="$,.0f", labels={"country": "Country", "annual_savings": "Annual Savings ($)"},
                )
                fig_g7.update_traces(
                    textposition="outside",
                    hovertemplate="<b>Country:</b> %{x}<br>Annual Savings: <b>$%{y:,.0f} / year</b><extra></extra>",
                )
                fig_g7.update_layout(**clean_plot_layout(height=300, show_legend=False))
                fig_g7.update_yaxes(range=[0, cmp_df["annual_savings"].max() * 1.25])
                st.plotly_chart(fig_g7, use_container_width=True, config=PLOT_CONFIG)

                st.markdown("""
                <div class="chart-takeaway-box">
                    <b>Analyst Finding:</b> Highlights real consumer pocketbook impact. High petrol tax nations (like Europe) deliver $1,000+ in annual fuel savings per driver.
                </div>
                """, unsafe_allow_html=True)

        with g_c8:
            with st.container(border=True):
                st.markdown(f"""
                <div class="chart-meta-overline">BENCHMARK #08 · CHARGER PROPORTION</div>
                <div class="chart-title-text">8. Charger Density: Public Chargers per 1,000 EVs ({bench_year})</div>
                <div class="chart-desc-text">Charging infrastructure availability relative to the size of the EV fleet</div>
                """, unsafe_allow_html=True)

                fig_g8 = px.bar(
                    cmp_df, x="country", y="chargers_per_1k_ev",
                    color="country", color_discrete_sequence=CHART_PALETTE,
                    text_auto=".0f", labels={"country": "Country", "chargers_per_1k_ev": "Chargers / 1k EVs"},
                )
                fig_g8.update_traces(
                    textposition="outside",
                    hovertemplate="<b>Country:</b> %{x}<br>Chargers per 1k EVs: <b>%{y:.0f}</b><extra></extra>",
                )
                fig_g8.update_layout(**clean_plot_layout(height=300, show_legend=False))
                fig_g8.update_yaxes(range=[0, cmp_df["chargers_per_1k_ev"].max() * 1.25])
                st.plotly_chart(fig_g8, use_container_width=True, config=PLOT_CONFIG)

                st.markdown("""
                <div class="chart-takeaway-box">
                    <b>Analyst Finding:</b> Compares network congestion. High ratios indicate surplus public charging capacity ready for new drivers.
                </div>
                """, unsafe_allow_html=True)

        # Row 5: Energy Prices & Road Transport CO2 Footprint
        g_c9, g_c10 = st.columns(2)
        with g_c9:
            with st.container(border=True):
                st.markdown(f"""
                <div class="chart-meta-overline">BENCHMARK #09 · ENERGY SPREAD</div>
                <div class="chart-title-text">9. Petrol Price vs. Electricity Price ({bench_year})</div>
                <div class="chart-desc-text">Petrol ($/Litre) alongside Electricity ($/kWh) for selected nations</div>
                """, unsafe_allow_html=True)

                fig_pe = go.Figure()
                fig_pe.add_trace(go.Bar(
                    name="Petrol ($/L)", x=cmp_df["country"], y=cmp_df["fuel_price_usd_per_liter"],
                    marker_color=COLORS["petrol"], text=cmp_df["fuel_price_usd_per_liter"].apply(lambda x: f"${x:.2f}"),
                    textposition="outside", hovertemplate="<b>Country:</b> %{x}<br>Petrol: <b>$%{y:.2f} / L</b><extra></extra>",
                ))
                fig_pe.add_trace(go.Bar(
                    name="Electricity ($/kWh)", x=cmp_df["country"], y=cmp_df["electricity_price_usd_per_kwh"],
                    marker_color=COLORS["primary"], text=cmp_df["electricity_price_usd_per_kwh"].apply(lambda x: f"${x:.2f}"),
                    textposition="outside", hovertemplate="<b>Country:</b> %{x}<br>Electricity: <b>$%{y:.2f} / kWh</b><extra></extra>",
                ))
                fig_pe.update_layout(**clean_plot_layout(height=300), barmode="group")
                st.plotly_chart(fig_pe, use_container_width=True, config=PLOT_CONFIG)

                st.markdown("""
                <div class="chart-takeaway-box">
                    <b>Analyst Finding:</b> Countries with high fossil fuel retail prices create strong financial pressure on drivers to choose electric mobility.
                </div>
                """, unsafe_allow_html=True)

        with g_c10:
            with st.container(border=True):
                st.markdown(f"""
                <div class="chart-meta-overline">BENCHMARK #10 · CARBON FOOTPRINT</div>
                <div class="chart-title-text">10. Transport Sector CO₂ Emissions (Mt CO₂ in {bench_year})</div>
                <div class="chart-desc-text">Total annual carbon emissions generated by passenger road transportation</div>
                """, unsafe_allow_html=True)

                fig_co2 = px.bar(
                    cmp_df, x="country", y="co2_emissions_transport_mt",
                    color="country", color_discrete_sequence=CHART_PALETTE,
                    text_auto=".1f", labels={"country": "Country", "co2_emissions_transport_mt": "Transport CO₂ (Mt)"},
                )
                fig_co2.update_traces(
                    textposition="outside",
                    hovertemplate="<b>Country:</b> %{x}<br>Transport Emissions: <b>%{y:.1f} Mt</b><extra></extra>",
                )
                fig_co2.update_layout(**clean_plot_layout(height=300, show_legend=False))
                fig_co2.update_yaxes(range=[0, cmp_df["co2_emissions_transport_mt"].max() * 1.25])
                st.plotly_chart(fig_co2, use_container_width=True, config=PLOT_CONFIG)

                st.markdown("""
                <div class="chart-takeaway-box">
                    <b>Analyst Finding:</b> Highlights the scale of emissions reduction required. Countries with large internal combustion fleets will experience major air quality improvements.
                </div>
                """, unsafe_allow_html=True)

        # Row 6: Policy Score & Battery Range
        g_c11, g_c12 = st.columns(2)
        with g_c11:
            with st.container(border=True):
                st.markdown(f"""
                <div class="chart-meta-overline">BENCHMARK #11 · POLICY MANDATES</div>
                <div class="chart-title-text">11. Vehicle Emission Regulation Stringency Score ({bench_year})</div>
                <div class="chart-desc-text">Government policy score evaluating fuel economy standards, ZEV mandates, and phase-out dates (0–100)</div>
                """, unsafe_allow_html=True)

                fig_pol = px.bar(
                    cmp_df, x="country", y="emission_regulation_score",
                    color="country", color_discrete_sequence=CHART_PALETTE,
                    text_auto=".0f", labels={"country": "Country", "emission_regulation_score": "Policy Score"},
                )
                fig_pol.update_traces(
                    textposition="outside",
                    hovertemplate="<b>Country:</b> %{x}<br>Regulation Score: <b>%{y:.0f} / 100</b><extra></extra>",
                )
                fig_pol.update_layout(**clean_plot_layout(height=300, show_legend=False))
                fig_pol.update_yaxes(range=[0, 115])
                st.plotly_chart(fig_pol, use_container_width=True, config=PLOT_CONFIG)

                st.markdown("""
                <div class="chart-takeaway-box">
                    <b>Analyst Finding:</b> Nations scoring above 80 on policy stringency implement aggressive fleet-wide penalties, directly inducing carmakers to prioritize electric delivery quotas.
                </div>
                """, unsafe_allow_html=True)

        with g_c12:
            with st.container(border=True):
                st.markdown(f"""
                <div class="chart-meta-overline">BENCHMARK #12 · BATTERY AUTONOMY</div>
                <div class="chart-title-text">12. Average Battery Range of EVs Sold ({bench_year})</div>
                <div class="chart-desc-text">Mean single-charge battery driving distance (km) for electric vehicles registered</div>
                """, unsafe_allow_html=True)

                fig_rng = px.bar(
                    cmp_df, x="country", y="avg_ev_range_km",
                    color="country", color_discrete_sequence=CHART_PALETTE,
                    text_auto=".0f", labels={"country": "Country", "avg_ev_range_km": "Range (km)"},
                )
                fig_rng.update_traces(
                    textposition="outside",
                    hovertemplate="<b>Country:</b> %{x}<br>Average Battery Range: <b>%{y:.0f} km</b><extra></extra>",
                )
                fig_rng.update_layout(**clean_plot_layout(height=300, show_legend=False))
                fig_rng.update_yaxes(range=[0, cmp_df["avg_ev_range_km"].max() * 1.25])
                st.plotly_chart(fig_rng, use_container_width=True, config=PLOT_CONFIG)

                st.markdown("""
                <div class="chart-takeaway-box">
                    <b>Analyst Finding:</b> Consumer range preference varies: long highway networks in North America demand larger battery packs (~500 km), whereas compact urban markets in Asia favor efficient city commuters.
                </div>
                """, unsafe_allow_html=True)

    # ── TAB 2: REGIONAL COMPARISON (MATCHING 12 HIGH-VALUE REGIONAL CHARTS) ──
    with tab_region:
        with st.container(border=True):
            rc_c1, rc_c2 = st.columns([3, 1])
            with rc_c1:
                st.markdown(
                    f'<div style="font-size: 0.95rem; font-weight: 600; color: #0F172A; padding-top: 0.35rem;">Comparing Continental Trading Blocs across 12 Identical Key Metrics: <b>Europe (14 nations)</b>, <b>Asia-Pacific (7 nations)</b>, and <b>Americas (4 nations)</b></div>',
                    unsafe_allow_html=True,
                )
            with rc_c2:
                reg_bench_year = st.selectbox(
                    "Observation Year",
                    options=sorted(all_years, reverse=True),
                    index=0,
                    key="cmp_reg_year_picker",
                )

        # Slice data strictly for the 3 regions
        reg_yr_df = df[(df["year"] == reg_bench_year) & (df["region"].isin(["Europe", "Asia-Pacific", "Americas"]))]
        reg_df = reg_yr_df.groupby("region", as_index=False).agg(
            avg_market_share=("ev_market_share", "mean"),
            total_sales=("ev_sales", "sum"),
            total_chargers=("charging_stations", "sum"),
            avg_subsidy=("ev_subsidy_usd", "mean"),
            petrol_sales=("petrol_car_sales", "sum"),
            diesel_sales=("diesel_car_sales", "sum"),
            avg_annual_savings=("annual_savings", "mean"),
            avg_fuel_price=("fuel_price_usd_per_liter", "mean"),
            avg_elec_price=("electricity_price_usd_per_kwh", "mean"),
            total_co2=("co2_emissions_transport_mt", "sum"),
            avg_policy_score=("emission_regulation_score", "mean"),
            avg_range=("avg_ev_range_km", "mean"),
        ).sort_values("avg_market_share", ascending=False)

        # Derived regional charger density
        reg_df["chargers_per_1k_ev"] = np.where(
            reg_df["total_sales"] > 0,
            (reg_df["total_chargers"] / reg_df["total_sales"]) * 1000.0,
            0.0
        )

        # Regional Row 1: EV Market Share vs Sales Volume
        rg_c1, rg_c2 = st.columns(2)
        with rg_c1:
            with st.container(border=True):
                st.markdown(f"""
                <div class="chart-meta-overline">REGIONAL BENCHMARK #01 · PENETRATION</div>
                <div class="chart-title-text">1. Average EV Adoption Rate by Region (% Share in {reg_bench_year})</div>
                <div class="chart-desc-text">Mean EV market share of passenger vehicles newly registered across continental trading blocs</div>
                """, unsafe_allow_html=True)

                fig_rg1 = px.bar(
                    reg_df, x="region", y="avg_market_share",
                    color="region", color_discrete_sequence=[COLORS["primary"], COLORS["green"], COLORS["petrol"]],
                    text_auto=".1f", labels={"region": "Region", "avg_market_share": "EV Share (%)"},
                )
                fig_rg1.update_traces(
                    textposition="outside",
                    hovertemplate="<b>Region:</b> %{x}<br>Average EV Share: <b>%{y:.1f}%</b><extra></extra>",
                )
                fig_rg1.update_layout(**clean_plot_layout(height=300, show_legend=False))
                fig_rg1.update_yaxes(range=[0, reg_df["avg_market_share"].max() * 1.25])
                st.plotly_chart(fig_rg1, use_container_width=True, config=PLOT_CONFIG)

                st.markdown("""
                <div class="chart-takeaway-box">
                    <b>Analyst Finding:</b> Europe maintains the highest average adoption rate (29.2%), driven by EU-wide corporate average emissions targets (95g CO₂/km) and binding national ICE phaseouts.
                </div>
                """, unsafe_allow_html=True)

        with rg_c2:
            with st.container(border=True):
                st.markdown(f"""
                <div class="chart-meta-overline">REGIONAL BENCHMARK #02 · PRODUCTION VOLUME</div>
                <div class="chart-title-text">2. Total EV Sales Volume by Region (Units sold in {reg_bench_year})</div>
                <div class="chart-desc-text">Total physical electric vehicles registered across each region</div>
                """, unsafe_allow_html=True)

                fig_rg2 = px.bar(
                    reg_df, x="region", y="total_sales",
                    color="region", color_discrete_sequence=[COLORS["primary"], COLORS["green"], COLORS["petrol"]],
                    labels={"region": "Region", "total_sales": "Total EV Sales"},
                )
                fig_rg2.update_traces(
                    hovertemplate="<b>Region:</b> %{x}<br>Total EV Sales: <b>%{y:,.0f} units</b><extra></extra>",
                )
                fig_rg2.update_layout(**clean_plot_layout(height=300, show_legend=False))
                st.plotly_chart(fig_rg2, use_container_width=True, config=PLOT_CONFIG)

                st.markdown("""
                <div class="chart-takeaway-box">
                    <b>Analyst Finding:</b> China's massive domestic automotive market propels Asia-Pacific to lead by far in raw units sold (surpassing 13M vehicles in 2025 alone).
                </div>
                """, unsafe_allow_html=True)

        # Regional Row 2: Charging Infrastructure Scale & Subsidies
        rg_c3, rg_c4 = st.columns(2)
        with rg_c3:
            with st.container(border=True):
                st.markdown(f"""
                <div class="chart-meta-overline">REGIONAL BENCHMARK #03 · NETWORK SCALE</div>
                <div class="chart-title-text">3. Public Charging Infrastructure Scale ({reg_bench_year})</div>
                <div class="chart-desc-text">Total public charging stations deployed across each continental region</div>
                """, unsafe_allow_html=True)

                fig_rg3 = px.bar(
                    reg_df, x="region", y="total_chargers",
                    color="region", color_discrete_sequence=[COLORS["primary"], COLORS["green"], COLORS["petrol"]],
                    labels={"region": "Region", "total_chargers": "Public Chargers"},
                )
                fig_rg3.update_traces(
                    hovertemplate="<b>Region:</b> %{x}<br>Public Chargers: <b>%{y:,.0f}</b><extra></extra>",
                )
                fig_rg3.update_layout(**clean_plot_layout(height=300, show_legend=False))
                st.plotly_chart(fig_rg3, use_container_width=True, config=PLOT_CONFIG)

                st.markdown("""
                <div class="chart-takeaway-box">
                    <b>Analyst Finding:</b> Asia-Pacific hosts the largest physical network of fast chargers (over 4.7M chargers), directly powering its high manufacturing throughput.
                </div>
                """, unsafe_allow_html=True)

        with rg_c4:
            with st.container(border=True):
                st.markdown(f"""
                <div class="chart-meta-overline">REGIONAL BENCHMARK #04 · FISCAL INCENTIVES</div>
                <div class="chart-title-text">4. Average Government EV Subsidy ($/Vehicle in {reg_bench_year})</div>
                <div class="chart-desc-text">Mean direct purchase incentive per vehicle provided by governments in USD</div>
                """, unsafe_allow_html=True)

                fig_rg4 = px.bar(
                    reg_df, x="region", y="avg_subsidy",
                    color="region", color_discrete_sequence=[COLORS["green"], COLORS["primary"], COLORS["petrol"]],
                    text_auto="$,.0f", labels={"region": "Region", "avg_subsidy": "Avg. Subsidy ($)"},
                )
                fig_rg4.update_traces(
                    textposition="outside",
                    hovertemplate="<b>Region:</b> %{x}<br>Avg. Subsidy: <b>$%{y:,.0f}</b><extra></extra>",
                )
                fig_rg4.update_layout(**clean_plot_layout(height=300, show_legend=False))
                fig_rg4.update_yaxes(range=[0, reg_df["avg_subsidy"].max() * 1.25])
                st.plotly_chart(fig_rg4, use_container_width=True, config=PLOT_CONFIG)

                st.markdown("""
                <div class="chart-takeaway-box">
                    <b>Analyst Finding:</b> The Americas and Europe have provided the highest upfront cash incentives, while Asian markets are pivoting towards infrastructure investments.
                </div>
                """, unsafe_allow_html=True)

        # Regional Row 3: 10-Year Progress Leap & Powertrain Fleet Mix
        rg_c5, rg_c6 = st.columns(2)
        with rg_c5:
            with st.container(border=True):
                st.markdown("""
                <div class="chart-meta-overline">REGIONAL BENCHMARK #05 · DECADE LEAP</div>
                <div class="chart-title-text">5. 10-Year Leap: Regional EV Share in 2015 vs. 2025</div>
                <div class="chart-desc-text">Direct grouped comparison showing decade adoption jumps across regions</div>
                """, unsafe_allow_html=True)

                reg_leap = df[
                    (df["year"].isin([2015, 2025])) &
                    (df["region"].isin(["Europe", "Asia-Pacific", "Americas"]))
                ].groupby(["region", "year"], as_index=False)["ev_market_share"].mean()
                reg_leap["year"] = reg_leap["year"].astype(str)

                fig_r5 = px.bar(
                    reg_leap, x="region", y="ev_market_share", color="year",
                    barmode="group", color_discrete_map={"2015": "#94A3B8", "2025": COLORS["ev"]},
                    text_auto=".1f", labels={"region": "Region", "ev_market_share": "EV Share (%)", "year": "Year"},
                )
                fig_r5.update_traces(
                    textposition="outside",
                    hovertemplate="<b>Region:</b> %{x} (%{data.name})<br>Avg. EV Share: <b>%{y:.1f}%</b><extra></extra>",
                )
                fig_r5.update_layout(**clean_plot_layout(height=300))
                st.plotly_chart(fig_r5, use_container_width=True, config=PLOT_CONFIG)

                st.markdown("""
                <div class="chart-takeaway-box">
                    <b>Analyst Finding:</b> Europe surged from 1.6% in 2015 to 29.2% in 2025, Asia-Pacific from 0.8% to 23.4%, and Americas from 0.7% to 15.6%.
                </div>
                """, unsafe_allow_html=True)

        with rg_c6:
            with st.container(border=True):
                st.markdown(f"""
                <div class="chart-meta-overline">REGIONAL BENCHMARK #06 · FLEET COMPOSITION</div>
                <div class="chart-title-text">6. Regional Powertrain Fleet Composition ({reg_bench_year})</div>
                <div class="chart-desc-text">Total vehicle sales broken down by Electric, Petrol, and Diesel</div>
                """, unsafe_allow_html=True)

                fig_r6 = go.Figure()
                fig_r6.add_trace(go.Bar(name="Electric (EV)", x=reg_df["region"], y=reg_df["total_sales"], marker_color=COLORS["ev"]))
                fig_r6.add_trace(go.Bar(name="Petrol", x=reg_df["region"], y=reg_df["petrol_sales"], marker_color=COLORS["petrol"]))
                fig_r6.add_trace(go.Bar(name="Diesel", x=reg_df["region"], y=reg_df["diesel_sales"], marker_color=COLORS["diesel"]))
                fig_r6.update_layout(**clean_plot_layout(height=300), barmode="stack", yaxis_title="Vehicles Sold")
                fig_r6.update_traces(hovertemplate="<b>Region:</b> %{x}<br><b>%{data.name}:</b> %{y:,.0f} units<extra></extra>")
                st.plotly_chart(fig_r6, use_container_width=True, config=PLOT_CONFIG)

                st.markdown("""
                <div class="chart-takeaway-box">
                    <b>Analyst Finding:</b> Electric vehicles now account for a significant portion of total registrations in all 3 trading blocs, eroding diesel demand.
                </div>
                """, unsafe_allow_html=True)

        # Regional Row 4: Annual Driver Fuel Savings & Charger Density
        rg_c7, rg_c8 = st.columns(2)
        with rg_c7:
            with st.container(border=True):
                st.markdown(f"""
                <div class="chart-meta-overline">REGIONAL BENCHMARK #07 · DRIVER ECONOMICS</div>
                <div class="chart-title-text">7. Annual Driver Fuel Cost Savings by Region ($/year in {reg_bench_year})</div>
                <div class="chart-desc-text">Average financial savings per EV driver per year (assuming 15,000 km driven)</div>
                """, unsafe_allow_html=True)

                fig_rg7 = px.bar(
                    reg_df, x="region", y="avg_annual_savings",
                    color="region", color_discrete_sequence=[COLORS["green"], COLORS["primary"], COLORS["petrol"]],
                    text_auto="$,.0f", labels={"region": "Region", "avg_annual_savings": "Annual Savings ($)"},
                )
                fig_rg7.update_traces(
                    textposition="outside",
                    hovertemplate="<b>Region:</b> %{x}<br>Annual Savings: <b>$%{y:,.0f} / year</b><extra></extra>",
                )
                fig_rg7.update_layout(**clean_plot_layout(height=300, show_legend=False))
                fig_rg7.update_yaxes(range=[0, reg_df["avg_annual_savings"].max() * 1.25])
                st.plotly_chart(fig_rg7, use_container_width=True, config=PLOT_CONFIG)

                st.markdown("""
                <div class="chart-takeaway-box">
                    <b>Analyst Finding:</b> European drivers save the most money per year (~$1,280/year) due to high petrol excise taxes, while American drivers save ~$900/year.
                </div>
                """, unsafe_allow_html=True)

        with rg_c8:
            with st.container(border=True):
                st.markdown(f"""
                <div class="chart-meta-overline">REGIONAL BENCHMARK #08 · CHARGER PROPORTION</div>
                <div class="chart-title-text">8. Regional Charger Density: Public Chargers per 1,000 EVs ({reg_bench_year})</div>
                <div class="chart-desc-text">Ratio of public charging infrastructure available relative to total EV sales</div>
                """, unsafe_allow_html=True)

                fig_rg8 = px.bar(
                    reg_df, x="region", y="chargers_per_1k_ev",
                    color="region", color_discrete_sequence=[COLORS["primary"], COLORS["green"], COLORS["petrol"]],
                    text_auto=".0f", labels={"region": "Region", "chargers_per_1k_ev": "Chargers / 1k EVs"},
                )
                fig_rg8.update_traces(
                    textposition="outside",
                    hovertemplate="<b>Region:</b> %{x}<br>Chargers per 1k EVs: <b>%{y:.0f}</b><extra></extra>",
                )
                fig_rg8.update_layout(**clean_plot_layout(height=300, show_legend=False))
                fig_rg8.update_yaxes(range=[0, reg_df["chargers_per_1k_ev"].max() * 1.25])
                st.plotly_chart(fig_rg8, use_container_width=True, config=PLOT_CONFIG)

                st.markdown("""
                <div class="chart-takeaway-box">
                    <b>Analyst Finding:</b> Asia-Pacific maintains high public charging ratios per EV, ensuring seamless intercity network access.
                </div>
                """, unsafe_allow_html=True)

        # Regional Row 5: Energy Prices & Road Transport CO2 Footprint
        rg_c9, rg_c10 = st.columns(2)
        with rg_c9:
            with st.container(border=True):
                st.markdown(f"""
                <div class="chart-meta-overline">REGIONAL BENCHMARK #09 · ENERGY DISPARITY</div>
                <div class="chart-title-text">9. Petrol Price vs. Electricity Price by Region ({reg_bench_year})</div>
                <div class="chart-desc-text">Average petrol price ($/Litre) alongside electricity rate ($/kWh)</div>
                """, unsafe_allow_html=True)

                fig_rg9 = go.Figure()
                fig_rg9.add_trace(go.Bar(
                    name="Petrol ($/L)", x=reg_df["region"], y=reg_df["avg_fuel_price"],
                    marker_color=COLORS["petrol"], text=reg_df["avg_fuel_price"].apply(lambda x: f"${x:.2f}"),
                    textposition="outside", hovertemplate="<b>Region:</b> %{x}<br>Petrol: <b>$%{y:.2f} / L</b><extra></extra>",
                ))
                fig_rg9.add_trace(go.Bar(
                    name="Electricity ($/kWh)", x=reg_df["region"], y=reg_df["avg_elec_price"],
                    marker_color=COLORS["primary"], text=reg_df["avg_elec_price"].apply(lambda x: f"${x:.2f}"),
                    textposition="outside", hovertemplate="<b>Region:</b> %{x}<br>Electricity: <b>$%{y:.2f} / kWh</b><extra></extra>",
                ))
                fig_rg9.update_layout(**clean_plot_layout(height=300), barmode="group")
                st.plotly_chart(fig_rg9, use_container_width=True, config=PLOT_CONFIG)

                st.markdown("""
                <div class="chart-takeaway-box">
                    <b>Analyst Finding:</b> European fuel taxes push retail petrol prices above $1.85/L, giving consumers an immediate economic justification to switch to electric vehicles.
                </div>
                """, unsafe_allow_html=True)

        with rg_c10:
            with st.container(border=True):
                st.markdown(f"""
                <div class="chart-meta-overline">REGIONAL BENCHMARK #10 · CARBON EMISSIONS</div>
                <div class="chart-title-text">10. Total Road Transport CO₂ Emissions by Region (Mt CO₂ in {reg_bench_year})</div>
                <div class="chart-desc-text">Cumulative passenger transport carbon emissions across each region</div>
                """, unsafe_allow_html=True)

                fig_rg10 = px.bar(
                    reg_df, x="region", y="total_co2",
                    color="region", color_discrete_sequence=[COLORS["red"], COLORS["petrol"], COLORS["diesel"]],
                    text_auto=".0f", labels={"region": "Region", "total_co2": "Transport CO₂ (Mt)"},
                )
                fig_rg10.update_traces(
                    textposition="outside",
                    hovertemplate="<b>Region:</b> %{x}<br>Transport CO₂: <b>%{y:,.1f} Mt</b><extra></extra>",
                )
                fig_rg10.update_layout(**clean_plot_layout(height=300, show_legend=False))
                fig_rg10.update_yaxes(range=[0, reg_df["total_co2"].max() * 1.25])
                st.plotly_chart(fig_rg10, use_container_width=True, config=PLOT_CONFIG)

                st.markdown("""
                <div class="chart-takeaway-box">
                    <b>Analyst Finding:</b> The Americas generate the highest aggregate transport emissions, underscoring the vital need to accelerate North American electrification.
                </div>
                """, unsafe_allow_html=True)

        # Regional Row 6: Policy Score & Battery Range
        rg_c11, rg_c12 = st.columns(2)
        with rg_c11:
            with st.container(border=True):
                st.markdown(f"""
                <div class="chart-meta-overline">REGIONAL BENCHMARK #11 · POLICY MANDATES</div>
                <div class="chart-title-text">11. Vehicle Emission Regulation Stringency Score (0–100 in {reg_bench_year})</div>
                <div class="chart-desc-text">Average policy stringency evaluating mandates, penalties, and zero-emission goals</div>
                """, unsafe_allow_html=True)

                fig_rg11 = px.bar(
                    reg_df, x="region", y="avg_policy_score",
                    color="region", color_discrete_sequence=[COLORS["purple"], COLORS["primary"], COLORS["petrol"]],
                    text_auto=".1f", labels={"region": "Region", "avg_policy_score": "Policy Stringency"},
                )
                fig_rg11.update_traces(
                    textposition="outside",
                    hovertemplate="<b>Region:</b> %{x}<br>Regulation Score: <b>%{y:.1f} / 100</b><extra></extra>",
                )
                fig_rg11.update_layout(**clean_plot_layout(height=300, show_legend=False))
                fig_rg11.update_yaxes(range=[0, 110])
                st.plotly_chart(fig_rg11, use_container_width=True, config=PLOT_CONFIG)

                st.markdown("""
                <div class="chart-takeaway-box">
                    <b>Analyst Finding:</b> Europe leads in regulatory stringency with strict Euro 7 fleet targets, establishing binding corporate decarbonization schedules.
                </div>
                """, unsafe_allow_html=True)

        with rg_c12:
            with st.container(border=True):
                st.markdown(f"""
                <div class="chart-meta-overline">REGIONAL BENCHMARK #12 · BATTERY AUTONOMY</div>
                <div class="chart-title-text">12. Average Battery Range of EVs Sold by Region (km in {reg_bench_year})</div>
                <div class="chart-desc-text">Mean single-charge battery driving range of electric vehicles sold</div>
                """, unsafe_allow_html=True)

                fig_rg12 = px.bar(
                    reg_df, x="region", y="avg_range",
                    color="region", color_discrete_sequence=[COLORS["green"], COLORS["primary"], COLORS["petrol"]],
                    text_auto=".0f", labels={"region": "Region", "avg_range": "Range (km)"},
                )
                fig_rg12.update_traces(
                    textposition="outside",
                    hovertemplate="<b>Region:</b> %{x}<br>Average Battery Range: <b>%{y:.0f} km</b><extra></extra>",
                )
                fig_rg12.update_layout(**clean_plot_layout(height=300, show_legend=False))
                fig_rg12.update_yaxes(range=[0, reg_df["avg_range"].max() * 1.25])
                st.plotly_chart(fig_rg12, use_container_width=True, config=PLOT_CONFIG)

                st.markdown("""
                <div class="chart-takeaway-box">
                    <b>Analyst Finding:</b> The Americas feature the highest average battery range (~495 km) due to extensive highway networks and larger vehicle classes (SUVs and trucks).
                </div>
                """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4: 📋 DATA TABLE & EXPORT
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📋 Data Table & Export":
    st.markdown("""
    <div class="page-header-container">
        <div class="page-eyebrow">DATASET EXPLORER / AUDIT & EXPORT</div>
        <div class="page-title">Dataset Explorer & CSV Export</div>
        <div class="page-desc">Inspect, search, and download the validated 25-country clean dataset (400 observations from 2010 to 2025).</div>
    </div>
    """, unsafe_allow_html=True)

    # Local Filters inside native container
    with st.container(border=True):
        st.markdown('<div class="chart-meta-overline">FILTER & SEARCH RECORDS</div>', unsafe_allow_html=True)
        t_f1, t_f2, t_f3 = st.columns([1, 1, 2])
        with t_f1:
            table_year = st.selectbox(
                "Filter by Year",
                options=["All Years (2010–2025)"] + [str(y) for y in sorted(all_years, reverse=True)],
                index=0,
                key="tbl_year_filter",
            )
        with t_f2:
            table_region = st.selectbox(
                "Filter by Region",
                options=["All Regions"] + all_regions,
                index=0,
                key="tbl_region_filter",
            )
        with t_f3:
            search_country = st.text_input("Search Country Name", placeholder="e.g. Norway, Germany, India, China...", key="tbl_search")

    # Slice data safely
    view_df = df.copy()
    if table_year != "All Years (2010–2025)":
        view_df = view_df[view_df["year"] == int(table_year)]
    if table_region != "All Regions":
        view_df = view_df[view_df["region"] == table_region]
    if search_country.strip():
        view_df = view_df[view_df["country"].str.contains(search_country.strip(), case=False, na=False)]

    # Metrics above table
    st_c1, st_c2, st_c3, st_c4 = st.columns(4)
    with st_c1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Matching Records</div>
            <div class="kpi-value">{len(view_df):,}</div>
            <div class="kpi-subtext">Rows in current view</div>
        </div>
        """, unsafe_allow_html=True)
    with st_c2:
        ev_val = fmt_val(view_df["ev_sales"].sum()) if not view_df.empty else "0"
        st.markdown(f"""
        <div class="kpi-card accent-blue">
            <div class="kpi-label">EV Sales Volume</div>
            <div class="kpi-value">{ev_val}</div>
            <div class="kpi-subtext">Sum in selection</div>
        </div>
        """, unsafe_allow_html=True)
    with st_c3:
        share_val = f"{view_df['ev_market_share'].mean():.1f}%" if not view_df.empty else "N/A"
        st.markdown(f"""
        <div class="kpi-card accent-emerald">
            <div class="kpi-label">Mean EV Share</div>
            <div class="kpi-value">{share_val}</div>
            <div class="kpi-subtext">Average market share</div>
        </div>
        """, unsafe_allow_html=True)
    with st_c4:
        chg_val = fmt_val(view_df["charging_stations"].sum()) if not view_df.empty else "0"
        st.markdown(f"""
        <div class="kpi-card accent-amber">
            <div class="kpi-label">Public Chargers</div>
            <div class="kpi-value">{chg_val}</div>
            <div class="kpi-subtext">Sum across selection</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)

    if view_df.empty:
        st.warning("⚠️ No records match your search query. Try clearing the search box or changing your filters.")
    else:
        display_cols = [
            "country", "year", "region", "ev_market_share", "ev_sales", "total_vehicle_sales",
            "charging_stations", "avg_ev_range_km", "fuel_price_usd_per_liter", "co2_emissions_transport_mt"
        ]
        raw_table = view_df[display_cols].sort_values(["year", "ev_market_share"], ascending=[False, False]).copy()

        # Cleanly formatted display version
        formatted_table = raw_table.copy()
        formatted_table.columns = [
            "Country", "Year", "Region", "EV Share (%)", "EV Sales", "Total Vehicle Sales",
            "Charging Stations", "Avg. Range (km)", "Petrol ($/L)", "Transport CO₂ (Mt)"
        ]
        formatted_table["EV Share (%)"] = formatted_table["EV Share (%)"].apply(lambda x: f"{x:.1f}%")
        formatted_table["EV Sales"] = formatted_table["EV Sales"].apply(lambda x: f"{x:,.0f}")
        formatted_table["Total Vehicle Sales"] = formatted_table["Total Vehicle Sales"].apply(lambda x: f"{x:,.0f}")
        formatted_table["Charging Stations"] = formatted_table["Charging Stations"].apply(lambda x: f"{x:,.0f}")
        formatted_table["Avg. Range (km)"] = formatted_table["Avg. Range (km)"].apply(lambda x: f"{x:.0f} km")
        formatted_table["Petrol ($/L)"] = formatted_table["Petrol ($/L)"].apply(lambda x: f"${x:.2f}")
        formatted_table["Transport CO₂ (Mt)"] = formatted_table["Transport CO₂ (Mt)"].apply(lambda x: f"{x:.1f}")

        st.dataframe(formatted_table, use_container_width=True, height=460)

        st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)
        st.download_button(
            label="📥 Export Dataset as CSV",
            data=raw_table.to_csv(index=False).encode("utf-8"),
            file_name=f"ev_market_data_{str(table_year).replace(' ', '_')}.csv",
            mime="text/csv",
        )


# ──────────────────────────────────────────────────────────────────────────────
# 6. FOOTER
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    ⚡ <b>FossilElectric · Electric Vehicle Market Intelligence Platform</b> · 25 Sovereign Economies · 2010–2025<br>
    Validated Empirical Dataset: <code>ev_vs_petrol_cleaned.csv</code> · Built with Python & Streamlit
</div>
""", unsafe_allow_html=True)
