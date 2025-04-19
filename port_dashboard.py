import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("your_dataset.csv")  # Change to actual file name

# Page config
st.set_page_config(page_title="Maritime Port Performance Dashboard", layout="wide")

# Title
st.title("📊 Maritime Port Performance Dashboard (2022–2023)")
st.markdown("This dashboard provides interactive insights into UNCTAD’s maritime port performance data (2022–2023).")

# Sidebar filters
st.sidebar.header("🔎 Filter Options")
vessel_types = st.sidebar.multiselect(
    "Select Vessel Type(s)", 
    options=df["vessel_type"].unique(),
    default=df["vessel_type"].unique()
)

periods = st.sidebar.multiselect(
    "Select Period(s)", 
    options=df["period"].unique(),
    default=df["period"].unique()
)

# Filter data
filtered_df = df[
    (df["vessel_type"].isin(vessel_types)) &
    (df["period"].isin(periods))
]

# KPIs section
st.subheader("📌 Key Performance Indicators (KPIs)")
kpi_col1, kpi_col2, kpi_col3 = st.columns(3)

try:
    kpi_col1.metric(
        label="Avg. Time in Port (Days)",
        value=f"{filtered_df['median_time_in_port'].mean():.2f}",
        help="Average median time vessels spend in port"
    )

    kpi_col2.metric(
        label="Avg. Vessel Age",
        value=f"{filtered_df['avg_vessel_age'].mean():.2f} yrs",
        help="Average vessel age during period"
    )

    kpi_col3.metric(
        label="Avg. Container Capacity (TEU)",
        value=f"{filtered_df['avg_container_capacity_TEU'].mean():,.0f}",
        help="Average container capacity in Twenty-foot Equivalent Units"
    )
except Exception as e:
    st.error(f"Error calculating KPIs: {e}")

st.markdown("---")

# Visualizations
st.subheader("📈 Visualizations")

# Select metric
metric_options = {
    "Avg. Time in Port": "median_time_in_port",
    "Avg. Vessel Age": "avg_vessel_age",
    "Avg. Size (GT)": "avg_size_GT",
    "Avg. Container Capacity (TEU)": "avg_container_capacity_TEU",
    "Avg. Cargo Capacity (DWT)": "avg_cargo_capacity_DWT"
}
metric_choice = st.selectbox("Choose Metric to Visualize", list(metric_options.keys()))
selected_column = metric_options[metric_choice]

# Line chart
fig = px.line(
    filtered_df.groupby(["period", "vessel_type"])[selected_column].mean().reset_index(),
    x="period",
    y=selected_column,
    color="vessel_type",
    markers=True,
    title=f"{metric_choice} Over Time by Vessel Type"
)
st.plotly_chart(fig, use_container_width=True)

# Summary
st.subheader("📝 Summary")
st.dataframe(filtered_df, use_container_width=True)

# Export Button
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode("utf-8")

csv = convert_df(filtered_df)
st.download_button(
    label="⬇️ Export Filtered Data as CSV",
    data=csv,
    file_name="filtered_port_performance.csv",
    mime="text/csv"
)

# Footer
st.markdown("🔹 *KPI: Key Performance Indicator — a metric summarizing an important performance attribute.*")
