import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from io import BytesIO

# ──────────────────────────────────────────────
#  PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Maritime Port Performance Dashboard",
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
#  GLOBAL STYLE INJECTION
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

/* ── Root tokens ── */
:root {
    --navy-900: #071829;
    --navy-800: #0A2342;
    --navy-700: #0D3260;
    --navy-600: #1B4F72;
    --mint-400: #00C9A7;
    --mint-300: #3DFFC0;
    --mint-100: #D0FFF4;
    --slate:    #E8EDF3;
    --text-primary: #071829;
    --text-secondary: #4A6080;
    --white: #FFFFFF;
    --card-shadow: 0 2px 16px rgba(7,24,41,0.10);
    --radius: 12px;
}

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--text-primary);
}

/* ── App background ── */
.stApp {
    background: linear-gradient(160deg, #EEF3F9 0%, #F5F9FC 100%);
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--navy-800) !important;
    border-right: 1px solid var(--navy-700);
}
section[data-testid="stSidebar"] * {
    color: #C9D8E8 !important;
}
section[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
    background: var(--mint-400) !important;
    color: var(--navy-900) !important;
}
section[data-testid="stSidebar"] a {
    color: var(--mint-400) !important;
    text-decoration: none;
    font-weight: 500;
    font-size: 0.85rem;
    line-height: 2;
}
section[data-testid="stSidebar"] a:hover {
    color: var(--mint-300) !important;
}

/* ── Sidebar headings ── */
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: var(--mint-400) !important;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    font-size: 0.75rem;
    margin-top: 1.4rem;
}

/* ── Main header banner ── */
.header-banner {
    background: linear-gradient(135deg, var(--navy-800) 0%, var(--navy-700) 60%, #0E4D6B 100%);
    border-radius: var(--radius);
    padding: 28px 36px;
    margin-bottom: 28px;
    display: flex;
    align-items: center;
    gap: 24px;
    box-shadow: var(--card-shadow);
    border-left: 5px solid var(--mint-400);
}
.header-banner img {
    border-radius: 50%;
    border: 3px solid var(--mint-400);
    width: 90px;
    height: 90px;
    object-fit: cover;
}
.header-title {
    color: var(--white);
    font-size: 1.75rem;
    font-weight: 700;
    margin: 0;
    letter-spacing: -0.01em;
}
.header-sub {
    color: var(--mint-400);
    font-size: 0.9rem;
    font-weight: 400;
    margin: 4px 0 0 0;
}

/* ── Section title ── */
.section-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--navy-800);
    border-left: 4px solid var(--mint-400);
    padding-left: 12px;
    margin: 32px 0 16px 0;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* ── KPI cards ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 8px;
}
.kpi-card {
    background: var(--white);
    border-radius: var(--radius);
    padding: 22px 24px;
    box-shadow: var(--card-shadow);
    border-top: 3px solid var(--mint-400);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 24px rgba(7,24,41,0.14);
}
.kpi-label {
    font-size: 0.72rem;
    font-weight: 600;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 8px;
}
.kpi-value {
    font-size: 1.9rem;
    font-weight: 700;
    color: var(--navy-800);
    font-family: 'DM Mono', monospace;
    line-height: 1;
}
.kpi-unit {
    font-size: 0.8rem;
    color: var(--text-secondary);
    font-weight: 400;
    margin-top: 4px;
}
.kpi-icon {
    font-size: 1.4rem;
    float: right;
    margin-top: -4px;
    opacity: 0.8;
}

/* ── Plot card wrapper ── */
.plot-card {
    background: var(--white);
    border-radius: var(--radius);
    padding: 20px 24px;
    box-shadow: var(--card-shadow);
    margin-bottom: 20px;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--slate);
    border-radius: 8px;
    padding: 4px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 6px;
    font-weight: 500;
    font-size: 0.85rem;
    color: var(--text-secondary);
}
.stTabs [aria-selected="true"] {
    background: var(--navy-800) !important;
    color: var(--mint-400) !important;
}

/* ── Selectbox / multiselect ── */
.stSelectbox label, .stMultiSelect label {
    font-weight: 600;
    font-size: 0.8rem;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

/* ── Download button ── */
.stDownloadButton > button {
    background: var(--mint-400) !important;
    color: var(--navy-900) !important;
    font-weight: 700;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-family: 'DM Sans', sans-serif;
    transition: background 0.2s;
}
.stDownloadButton > button:hover {
    background: var(--mint-300) !important;
}

/* ── Footer ── */
.footer {
    text-align: center;
    padding: 24px;
    margin-top: 40px;
    background: var(--navy-800);
    border-radius: var(--radius);
    color: #7A9BB5;
    font-size: 0.8rem;
    border-top: 2px solid var(--mint-400);
}
.footer span {
    color: var(--mint-400);
    font-weight: 600;
}

/* ── Anchor targets ── */
.anchor { padding-top: 70px; margin-top: -70px; display: block; }

/* ── Dataframe ── */
.stDataFrame { border-radius: var(--radius); overflow: hidden; }

/* ── Alert / info boxes ── */
.stAlert {
    border-radius: var(--radius);
    border-left: 4px solid var(--mint-400);
}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
#  CHART THEME
# ──────────────────────────────────────────────
NAVY      = "#0A2342"
MINT      = "#00C9A7"
NAVY_MID  = "#1B4F72"
PALETTE   = [MINT, "#005F73", "#0A9396", "#94D2BD", "#E9D8A6", "#EE9B00", "#CA6702"]

plt.rcParams.update({
    "figure.facecolor":  "white",
    "axes.facecolor":    "#F5F9FC",
    "axes.edgecolor":    "#DDE4EC",
    "axes.labelcolor":   NAVY,
    "axes.titlecolor":   NAVY,
    "axes.titlesize":    13,
    "axes.titleweight":  "bold",
    "axes.titlepad":     14,
    "axes.labelsize":    10,
    "xtick.color":       "#4A6080",
    "ytick.color":       "#4A6080",
    "xtick.labelsize":   9,
    "ytick.labelsize":   9,
    "grid.color":        "#DDE4EC",
    "grid.linewidth":    0.6,
    "legend.fontsize":   9,
    "legend.framealpha": 0.9,
    "legend.edgecolor":  "#DDE4EC",
    "font.family":       "sans-serif",
})
sns.set_palette(PALETTE)

# ──────────────────────────────────────────────
#  DATA LOADER
# ──────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_port_performance_dataset_2022_2023.csv")
    df.columns = df.columns.str.strip().str.lower()
    return df

df = load_data()

METRIC_LABELS = {
    "median_time_in_port":   "Median Time in Port (Days)",
    "avg_vessel_age":        "Avg. Vessel Age (Years)",
    "avg_cargo_capacity_dwt":"Avg. Cargo Capacity (DWT)",
    "avg_size_gt":           "Avg. Vessel Size (GT)",
}

# ──────────────────────────────────────────────
#  SIDEBAR — TOC + FILTERS
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚓ Navigation")
    st.markdown("""
    <a href="#overview">📌 Overview & KPIs</a><br>
    <a href="#trend">📈 Trend Analysis</a><br>
    <a href="#distribution">📦 Distribution</a><br>
    <a href="#comparison">🔁 Comparison</a><br>
    <a href="#histogram">📊 Metric Distribution</a><br>
    <a href="#data">🗄️ Raw Data</a><br>
    <a href="#export">📤 Export</a>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## 🔎 Filters")

    vessel_types = df["vessel_type"].dropna().unique().tolist()
    selected_vessels = st.multiselect(
        "Vessel Type(s)",
        options=vessel_types,
        default=vessel_types,
    )

    periods = df["period"].dropna().unique().tolist()
    selected_periods = st.multiselect(
        "Period(s)",
        options=periods,
        default=periods,
    )

    st.markdown("---")
    st.markdown("## 📐 Chart Options")
    plot_type = st.selectbox(
        "Plot Type",
        ["Bar Chart", "Line Plot", "Box Plot"],
    )
    metric = st.selectbox(
        "Primary Metric",
        list(METRIC_LABELS.keys()),
        format_func=lambda x: METRIC_LABELS[x],
    )

# ──────────────────────────────────────────────
#  FILTERED DATA
# ──────────────────────────────────────────────
filtered_df = df[
    df["vessel_type"].isin(selected_vessels) &
    df["period"].isin(selected_periods)
]

# ──────────────────────────────────────────────
#  HEADER BANNER
# ──────────────────────────────────────────────
st.markdown("""
<div class="header-banner">
    <img src="Port.png" alt="Port Logo" onerror="this.style.display='none'">
    <div>
        <p class="header-title">⚓ Maritime Port Performance Dashboard</p>
        <p class="header-sub">2022 – 2023 · Vessel Analytics · TopTech Dynamics Limited</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Fallback if PNG can't render inline via HTML (Streamlit local files)
try:
    col_logo, col_title = st.columns([1, 6])
    with col_logo:
        st.image("Port.png", width=90)
    with col_title:
        st.write("")  # vertical spacer
except Exception:
    pass

if filtered_df.empty:
    st.warning("No data matches your current filter selection. Please adjust the sidebar filters.")
    st.stop()

# ──────────────────────────────────────────────
#  SECTION 1 — KPIs
# ──────────────────────────────────────────────
st.markdown('<a class="anchor" id="overview"></a>', unsafe_allow_html=True)
st.markdown('<div class="section-title">📌 Overview & Key Performance Indicators</div>', unsafe_allow_html=True)

avg_time = filtered_df["median_time_in_port"].mean()
avg_age  = filtered_df["avg_vessel_age"].mean()
avg_dwt  = filtered_df["avg_cargo_capacity_dwt"].mean()
avg_gt   = filtered_df["avg_size_gt"].mean()
n_types  = filtered_df["vessel_type"].nunique()
n_rows   = len(filtered_df)

st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi-card">
        <span class="kpi-icon">🕐</span>
        <div class="kpi-label">Avg. Time in Port</div>
        <div class="kpi-value">{avg_time:.1f}</div>
        <div class="kpi-unit">days (median)</div>
    </div>
    <div class="kpi-card">
        <span class="kpi-icon">🚢</span>
        <div class="kpi-label">Avg. Vessel Age</div>
        <div class="kpi-value">{avg_age:.1f}</div>
        <div class="kpi-unit">years</div>
    </div>
    <div class="kpi-card">
        <span class="kpi-icon">📦</span>
        <div class="kpi-label">Avg. Cargo Capacity</div>
        <div class="kpi-value">{int(avg_dwt):,}</div>
        <div class="kpi-unit">DWT</div>
    </div>
    <div class="kpi-card">
        <span class="kpi-icon">📐</span>
        <div class="kpi-label">Avg. Vessel Size</div>
        <div class="kpi-value">{int(avg_gt):,}</div>
        <div class="kpi-unit">Gross Tonnage (GT)</div>
    </div>
    <div class="kpi-card">
        <span class="kpi-icon">🔖</span>
        <div class="kpi-label">Vessel Types</div>
        <div class="kpi-value">{n_types}</div>
        <div class="kpi-unit">categories selected</div>
    </div>
    <div class="kpi-card">
        <span class="kpi-icon">📋</span>
        <div class="kpi-label">Records in View</div>
        <div class="kpi-value">{n_rows:,}</div>
        <div class="kpi-unit">filtered rows</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
#  SECTION 2 — TREND / DISTRIBUTION / COMPARISON
# ──────────────────────────────────────────────
st.markdown('<a class="anchor" id="trend"></a>', unsafe_allow_html=True)
st.markdown('<div class="section-title">📈 Performance Analysis</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Trend Analysis", "Distribution", "Comparison"])

def style_axis(ax, title=""):
    ax.set_title(title, pad=14)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#DDE4EC")
    for label in ax.get_xticklabels():
        label.set_rotation(30)
        label.set_ha("right")

with tab1:
    st.markdown('<a class="anchor" id="trend-inner"></a>', unsafe_allow_html=True)
    fig1, ax1 = plt.subplots(figsize=(11, 5))
    title_str = f"{METRIC_LABELS[metric]} by Period"

    if plot_type == "Line Plot":
        sns.lineplot(
            data=filtered_df, x="period", y=metric,
            hue="vessel_type", style="vessel_type",
            markers=True, linewidth=2.2, ax=ax1,
        )
    elif plot_type == "Bar Chart":
        sns.barplot(
            data=filtered_df, x="period", y=metric,
            hue="vessel_type", ax=ax1, edgecolor="white",
            linewidth=0.6,
        )
    else:  # Box Plot
        sns.boxplot(
            data=filtered_df, x="period", y=metric,
            hue="vessel_type", ax=ax1, linewidth=1.2,
            flierprops=dict(marker="o", markersize=4, alpha=0.5),
        )

    style_axis(ax1, title_str)
    ax1.set_xlabel("Period", labelpad=8)
    ax1.set_ylabel(METRIC_LABELS[metric], labelpad=8)
    ax1.legend(
        title="Vessel Type", bbox_to_anchor=(1.01, 1),
        loc="upper left", borderaxespad=0,
    )
    fig1.tight_layout()
    st.pyplot(fig1)

with tab2:
    st.markdown('<a class="anchor" id="distribution"></a>', unsafe_allow_html=True)
    fig2, ax2 = plt.subplots(figsize=(11, 5))
    sns.boxplot(
        data=filtered_df, x="vessel_type", y=metric,
        palette=PALETTE, ax=ax2, linewidth=1.2,
        flierprops=dict(marker="o", markersize=4, alpha=0.5),
    )
    style_axis(ax2, f"Distribution of {METRIC_LABELS[metric]} by Vessel Type")
    ax2.set_xlabel("Vessel Type", labelpad=8)
    ax2.set_ylabel(METRIC_LABELS[metric], labelpad=8)
    fig2.tight_layout()
    st.pyplot(fig2)

with tab3:
    st.markdown('<a class="anchor" id="comparison"></a>', unsafe_allow_html=True)
    compare_options = [m for m in METRIC_LABELS if m != metric]
    compare_metric = st.selectbox(
        "Compare With",
        compare_options,
        format_func=lambda x: METRIC_LABELS[x],
    )
    fig3, ax3 = plt.subplots(figsize=(11, 5))
    sns.scatterplot(
        data=filtered_df,
        x=metric, y=compare_metric,
        hue="vessel_type", size="avg_size_gt",
        sizes=(40, 280), alpha=0.75, ax=ax3,
        palette=PALETTE,
    )
    style_axis(ax3, f"{METRIC_LABELS[metric]}  vs  {METRIC_LABELS[compare_metric]}")
    ax3.set_xlabel(METRIC_LABELS[metric], labelpad=8)
    ax3.set_ylabel(METRIC_LABELS[compare_metric], labelpad=8)
    ax3.legend(
        title="Vessel Type", bbox_to_anchor=(1.01, 1),
        loc="upper left", borderaxespad=0,
    )
    fig3.tight_layout()
    st.pyplot(fig3)

# ──────────────────────────────────────────────
#  SECTION 3 — HISTOGRAM
# ──────────────────────────────────────────────
st.markdown('<a class="anchor" id="histogram"></a>', unsafe_allow_html=True)
st.markdown('<div class="section-title">📊 Metric Distribution</div>', unsafe_allow_html=True)

fig4, ax4 = plt.subplots(figsize=(11, 4))
sns.histplot(
    filtered_df[metric], kde=True, bins=18,
    color=MINT, edgecolor="white", linewidth=0.5, ax=ax4,
    line_kws={"linewidth": 2.2, "color": NAVY},
)
ax4.set_xlabel(METRIC_LABELS[metric], labelpad=8)
ax4.set_ylabel("Frequency", labelpad=8)
ax4.set_title(f"Frequency Distribution — {METRIC_LABELS[metric]}", pad=14)
ax4.spines[["top", "right"]].set_visible(False)
ax4.spines[["left", "bottom"]].set_color("#DDE4EC")
fig4.tight_layout()
st.pyplot(fig4)

# ──────────────────────────────────────────────
#  SECTION 4 — RAW DATA TABLE
# ──────────────────────────────────────────────
st.markdown('<a class="anchor" id="data"></a>', unsafe_allow_html=True)
st.markdown('<div class="section-title">🗄️ Filtered Data Table</div>', unsafe_allow_html=True)

display_cols = [c for c in ["vessel_type", "period"] + list(METRIC_LABELS.keys()) if c in filtered_df.columns]
st.dataframe(
    filtered_df[display_cols]
    .rename(columns={**METRIC_LABELS, "vessel_type": "Vessel Type", "period": "Period"})
    .reset_index(drop=True),
    use_container_width=True,
    height=260,
)

# ──────────────────────────────────────────────
#  SECTION 5 — EXPORT
# ──────────────────────────────────────────────
st.markdown('<a class="anchor" id="export"></a>', unsafe_allow_html=True)
st.markdown('<div class="section-title">📤 Export Data</div>', unsafe_allow_html=True)

@st.cache_data
def convert_df_to_excel(dataframe: pd.DataFrame) -> bytes:
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        dataframe.to_excel(writer, index=False, sheet_name="Port Performance")
        workbook  = writer.book
        worksheet = writer.sheets["Port Performance"]
        header_fmt = workbook.add_format({
            "bold": True, "bg_color": "#0A2342", "font_color": "#00C9A7",
            "border": 1, "align": "center",
        })
        for col_num, value in enumerate(dataframe.columns):
            worksheet.write(0, col_num, value, header_fmt)
            worksheet.set_column(col_num, col_num, 22)
    return output.getvalue()

col_exp1, col_exp2 = st.columns([2, 3])
with col_exp1:
    excel_data = convert_df_to_excel(filtered_df)
    st.download_button(
        label="📥 Download Filtered Data (.xlsx)",
        data=excel_data,
        file_name="port_performance_filtered.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
with col_exp2:
    st.info(f"Exporting **{len(filtered_df):,}** records across **{filtered_df['vessel_type'].nunique()}** vessel type(s) and **{filtered_df['period'].nunique()}** period(s).")

# ──────────────────────────────────────────────
#  FOOTER
# ──────────────────────────────────────────────
st.markdown("""
<div class="footer">
    © 2025 <span>TopTech Dynamics Limited</span> &nbsp;|&nbsp; Maritime Port Performance Intelligence
    &nbsp;|&nbsp; Analytics for Informed Decisions
</div>
""", unsafe_allow_html=True)
