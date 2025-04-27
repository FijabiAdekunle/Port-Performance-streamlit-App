import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

st.write("Dataset columns:", df.columns.tolist())

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
    df.columns = df.columns.str.strip()
    return df

df = load_data()

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
st.markdown("This dashboard provides interactive insights into UNCTAD’s maritime port performance data (2022–2023).")

# KPI Section
st.subheader("📌 Key Performance Indicators (KPIs)")

col1, col2, col3 = st.columns(3)

avg_time = filtered_df["Median_time_in_port_days_Value"].mean()
avg_age = filtered_df["Average_age_of_vessels_years_Value"].mean()
avg_teu = filtered_df["Average_cargo_carrying_capacity_dwt_per_vessel_Value"].mean() 

col1.metric("Avg. Time in Port (Days)", f"{avg_time:.1f}" if not pd.isna(avg_time) else "N/A")
col2.metric("Avg. Vessel Age", f"{avg_age:.1f} yrs" if not pd.isna(avg_age) else "N/A")
col3.metric("Avg. Cargo Capacity (DWT)", f"{int(avg_teu):,}" if not pd.isna(avg_teu) else "N/A") 

st.info("💡 **KPI** = Key Performance Indicator — a metric summarizing an important performance attribute.")

# Visualizations
st.subheader("📈 Visualizations")

metric_choice = st.selectbox("Choose a metric to visualize", [
    "Median_time_in_port_days_Value",
    "Average_age_of_vessels_years_Value",
    "Average_cargo_carrying_capacity_dwt_per_vessel_Value",
    "Average_size_GT_of_vessels_Value",
    "Maximum_cargo_carrying_capacity_dwt_of_vessels_Value"
])

st.caption("Metric displayed across vessel types and periods.")

if not filtered_df.empty:
    grouped_df = (
        filtered_df.groupby(["period", "vessel_type"])[metric_choice]
        .mean()
        .reset_index()
    )
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=grouped_df, x="period", y=metric_choice, hue="vessel_type", marker="o")
    plt.title(f"{metric_choice.replace('_', ' ').title()} Over Time by Vessel Type")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt.gcf())
else:
    st.warning("No data available for the selected filters.")

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
