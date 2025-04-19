import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned data
df = pd.read_csv("us_port_cleaned_dataset.csv")

st.set_page_config(page_title="Maritime Port Dashboard", layout="wide")

# --- Sidebar Filters ---
st.sidebar.header("🔎 Filter Options")
vessel_options = df['vessel_type'].unique()
period_options = df['period'].unique()

selected_vessel = st.sidebar.multiselect("Select Vessel Type(s)", vessel_options, default=vessel_options)
selected_period = st.sidebar.multiselect("Select Period(s)", period_options, default=period_options)

# Filter Data
filtered_df = df[df['vessel_type'].isin(selected_vessel) & df['period'].isin(selected_period)]

# --- Tabs Layout ---
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📈 Visualizations", "📝 Summary"])

# ========== TAB 1: DASHBOARD ==========
with tab1:
    st.title("📊 Maritime Port Performance Dashboard (2022–2023)")
    st.markdown("This dashboard provides interactive insights into UNCTAD’s maritime port performance data (2022–2023).")
    
    # --- KPI Section ---
    st.subheader("📌 Key Performance Indicators (KPIs)")

    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Avg. Time in Port (Days)", f"{filtered_df['median_time_in_port'].mean():.1f}")
    kpi2.metric("Avg. Vessel Age", f"{filtered_df['avg_vessel_age'].mean():.1f} yrs")
    kpi3.metric("Avg. Container Capacity (TEU)", f"{filtered_df['avg_container_capacity_TEU'].mean():,.0f}")

    # --- Tooltip help ---
    st.help("KPI: Key Performance Indicator — a metric summarizing an important performance attribute.")

    # --- Export Button ---
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Export Filtered Data to CSV", data=csv, file_name="filtered_port_data.csv", mime='text/csv')

# ========== TAB 2: VISUALIZATIONS ==========
with tab2:
    st.header("📈 Interactive Visualizations")

    # Select plot
    plot_type = st.selectbox("Choose a plot to display", [
        "Boxplot: Time in Port by Vessel Type",
        "Boxplot: Average Size (GT) by Vessel Type",
        "Boxplot: Time in Port by Period",
        "Boxplot: Average Size (GT) by Period",
        "Correlation Heatmap"
    ])

    if plot_type == "Boxplot: Time in Port by Vessel Type":
        fig, ax = plt.subplots(figsize=(10,5))
        sns.boxplot(x='vessel_type', y='median_time_in_port', data=filtered_df, ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    elif plot_type == "Boxplot: Average Size (GT) by Vessel Type":
        fig, ax = plt.subplots(figsize=(10,5))
        sns.boxplot(x='vessel_type', y='avg_size_GT', data=filtered_df, ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    elif plot_type == "Boxplot: Time in Port by Period":
        fig, ax = plt.subplots(figsize=(10,5))
        sns.boxplot(x='period', y='median_time_in_port', data=filtered_df, ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    elif plot_type == "Boxplot: Average Size (GT) by Period":
        fig, ax = plt.subplots(figsize=(10,5))
        sns.boxplot(x='period', y='avg_size_GT', data=filtered_df, ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    elif plot_type == "Correlation Heatmap":
        numerical_cols = filtered_df.select_dtypes(include='number')
        fig, ax = plt.subplots(figsize=(12,10))
        sns.heatmap(numerical_cols.corr(), annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)

    # --- Line Chart Section ---
    st.subheader("📉 Line Chart: Compare Metrics Across Vessel Types")

    metric_choice = st.selectbox(
        "Choose a metric",
        ['median_time_in_port', 'avg_size_GT', 'avg_cargo_capacity_DWT', 'avg_container_capacity_TEU']
    )

    line_df = filtered_df.groupby("vessel_type")[metric_choice].mean().reset_index()
    fig_line, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=line_df, x='vessel_type', y=metric_choice, marker='o', ax=ax)
    plt.xticks(rotation=45)
    plt.title(f"{metric_choice} by Vessel Type")
    st.pyplot(fig_line)

# ========== TAB 3: SUMMARY ==========
with tab3:
    st.header("📝 Summary of Findings")
    st.markdown("""
    ### 📌 EDA Insights
    - **Vessel Age**: Average age ~15–18 years. Container and LNG ships tend to be newer.
    - **Time in Port**: Container ships are faster in turnaround; Breakbulk and passenger ships stay longer.
    - **Vessel Size & Capacity**: Larger GT often corresponds with higher cargo (DWT) and container (TEU) capacities.
    - **Period Consistency**: Stable metrics across 2022–2023; no drastic performance shifts.

    ### 📌 Summary
    - **Container ships** appear most efficient in port time.
    - **LNG carriers** show larger average sizes.
    - **Operational consistency** was maintained across both years.
    - Dataset suitable for clustering or unsupervised ML in future.
    """)
