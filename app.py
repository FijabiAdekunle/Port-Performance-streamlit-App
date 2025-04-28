import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

# Page config
st.set_page_config(
    page_title="Maritime Port Performance Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_port_performance_dataset_2022_2023.csv")
    df.columns = df.columns.str.strip().str.lower()  # Normalize to lowercase
    return df

df = load_data()

# Show columns for debugging (remove in production)
st.write("Available columns:", df.columns.tolist())

# Sidebar filters
st.sidebar.title("🔎 Filter Options")

vessel_types = df["vessel_type"].dropna().unique().tolist()
selected_vessels = st.sidebar.multiselect(
    "Select Vessel Type(s)",
    options=vessel_types,
    default=vessel_types,
)

periods = df["period"].dropna().unique().tolist()
selected_periods = st.sidebar.multiselect(
    "Select Period(s)",
    options=periods,
    default=periods,
)

# Filter data
filtered_df = df[
    (df["vessel_type"].isin(selected_vessels)) &
    (df["period"].isin(selected_periods))
]

# Header
st.title("📊 Maritime Port Performance Dashboard (2022–2023)")

# KPI Section - USING CORRECT COLUMN NAMES
st.subheader("📌 Key Performance Indicators (KPIs)")
col1, col2, col3 = st.columns(3)

avg_time = filtered_df["median_time_in_port"].mean()
avg_age = filtered_df["avg_vessel_age"].mean()
avg_dwt = filtered_df["avg_cargo_capacity_dwt"].mean()

col1.metric("Avg. Time in Port (Days)", f"{avg_time:.1f}")
col2.metric("Avg. Vessel Age", f"{avg_age:.1f} yrs")
col3.metric("Avg. Cargo Capacity (DWT)", f"{int(avg_dwt):,}")

# Visualizations - USING CORRECT COLUMN NAMES
st.subheader("📈 Visualizations")
metric_choice = st.selectbox("Choose a metric to visualize", [
    "median_time_in_port",
    "avg_vessel_age",
    "avg_cargo_capacity_dwt",
    "avg_size_gt",
    "max_cargo_capacity_dwt"
])

if not filtered_df.empty:
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(
        data=filtered_df,
        x="period",
        y=metric_choice,
        hue="vessel_type",
        marker="o",
        ax=ax
    )
    ax.set_title(f"{metric_choice.replace('_', ' ').title()} Over Time")
    plt.xticks(rotation=45)
    st.pyplot(fig)
else:
    st.warning("No data available for selected filters.")


# Export button
st.subheader("📤 Export Data")

@st.cache_data

def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Filtered Data')
    processed_data = output.getvalue()
    return processed_data

if not filtered_df.empty:
    excel_data = convert_df_to_excel(filtered_df)
    st.download_button(
        label="📥 Download Filtered Data as Excel",
        data=excel_data,
        file_name='filtered_port_data.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

# Summary
st.subheader("📝 Summary")
st.markdown("""
This dashboard offers stakeholders an overview of vessel performance indicators such as:
- Time spent in ports
- Average vessel age
- Container and cargo capacity

Use this tool to monitor port performance trends across various vessel types and time periods.
""")
# === FOOTER ===
st.markdown("""
---
<small>© 2025 TopTech Digital Intelligence LLC | Analytics for informed decisions</small>
""", unsafe_allow_html=True)