import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned data
df = pd.read_csv("us_port_cleaned_dataset.csv")

# Sidebar filters
st.sidebar.header("🔍 Filter Data")
vessel_types = df["vessel_type"].unique()
periods = df["period"].unique()
selected_vessel = st.sidebar.selectbox("Select Vessel Type", ["All"] + list(vessel_types))
selected_period = st.sidebar.selectbox("Select Period", ["All"] + list(periods))

# Apply filters
filtered_df = df.copy()
if selected_vessel != "All":
    filtered_df = filtered_df[filtered_df["vessel_type"] == selected_vessel]
if selected_period != "All":
    filtered_df = filtered_df[filtered_df["period"] == selected_period]

# Page title and intro
st.title("📊 Maritime Port Performance Dashboard (2022–2023)")
st.markdown("""
Welcome to the interactive dashboard that showcases insights from the UNCTAD Maritime Port Performance dataset.
This app helps visualize vessel trends, port efficiency, and key statistics from 2022–2023.
""")

# Summary box
st.markdown("""
> **Project Summary**  
> - Dataset: UNCTAD Maritime Port Statistics (2022–2023)  
> - Focus: Vessel turnaround time, average ship size, operational consistency
""")

# Key Insights
st.header("📌 Key EDA Insights")
st.markdown("""
- **Vessel Age**: Average age ~15–18 years. Container and LNG ships tend to be newer.
- **Time in Port**: Container ships are faster in turnaround; Breakbulk and passenger ships stay longer.
- **Vessel Size & Capacity**: Larger GT often corresponds with higher cargo (DWT) and container (TEU) capacities.
- **Period Consistency**: Stable metrics across 2022–2023; no drastic performance shifts.
""")

# Tabs layout
plot_tabs = st.tabs(["Boxplots", "Correlation", "Capacity Comparison", "Narrative"])

# Boxplots Tab
with plot_tabs[0]:
    st.subheader("📦 Boxplots")
    plot_type = st.selectbox("Choose a boxplot to display", [
        "Time in Port by Vessel Type",
        "Average Size (GT) by Vessel Type",
        "Time in Port by Period",
        "Average Size (GT) by Period"
    ])

    if plot_type == "Time in Port by Vessel Type":
        fig, ax = plt.subplots(figsize=(10,5))
        sns.boxplot(x='vessel_type', y='median_time_in_port', data=filtered_df, ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    elif plot_type == "Average Size (GT) by Vessel Type":
        fig, ax = plt.subplots(figsize=(10,5))
        sns.boxplot(x='vessel_type', y='avg_size_GT', data=filtered_df, ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    elif plot_type == "Time in Port by Period":
        fig, ax = plt.subplots(figsize=(10,5))
        sns.boxplot(x='period', y='median_time_in_port', data=filtered_df, ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    elif plot_type == "Average Size (GT) by Period":
        fig, ax = plt.subplots(figsize=(10,5))
        sns.boxplot(x='period', y='avg_size_GT', data=filtered_df, ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

# Correlation Tab
with plot_tabs[1]:
    st.subheader("🔗 Correlation Heatmap")
    numerical_cols = filtered_df.select_dtypes(include='number')
    fig, ax = plt.subplots(figsize=(12,10))
    sns.heatmap(numerical_cols.corr(), annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)

# Capacity Comparison Tab
with plot_tabs[2]:
    st.subheader("📊 Compare Vessel Capacities (TEU / DWT / GT)")
    metric_choice = st.selectbox("Select Metric to Compare", ["avg_teu", "avg_dwt", "avg_size_GT"])
    comp_df = (
        filtered_df.groupby("vessel_type")[metric_choice]
        .mean()
        .reset_index()
        .sort_values(by=metric_choice, ascending=False)
    )
    fig7, ax7 = plt.subplots(figsize=(10,5))
    sns.barplot(x=metric_choice, y="vessel_type", data=comp_df, ax=ax7, palette="viridis")
    ax7.set_title(f"Average {metric_choice.upper()} by Vessel Type")
    st.pyplot(fig7)

# Narrative Tab
with plot_tabs[3]:
    st.subheader("📘 Maritime Analytics Narrative")
    st.markdown("""
    ### Project Summary

    This dashboard presents key insights from the UNCTAD port performance data for 2022–2023. It focuses on:
    - Turnaround times by vessel types
    - Vessel capacity comparisons
    - Operational trends over time

    ### Recommendations
    - Encourage modernization of older vessel types.
    - Identify ports with long turnaround times for process optimization.
    - Explore clustering to group ports or vessels by efficiency patterns.

    Data serves as a strong foundation for forecasting, optimization, and benchmarking within maritime logistics.
    """)
