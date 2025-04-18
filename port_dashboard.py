import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned data
df = pd.read_csv("us_port_cleaned_dataset.csv")  

# Sidebar filters
st.sidebar.header("🔎 Filter Data")
vessel_types = ['All'] + sorted(df['vessel_type'].unique())
selected_vessel = st.sidebar.selectbox("Select Vessel Type", vessel_types)

periods = ['All'] + sorted(df['period'].unique())
selected_period = st.sidebar.selectbox("Select Period", periods)

# Apply filters
filtered_df = df.copy()
if selected_vessel != 'All':
    filtered_df = filtered_df[filtered_df['vessel_type'] == selected_vessel]
if selected_period != 'All':
    filtered_df = filtered_df[filtered_df['period'] == selected_period]

# Page title and intro
st.title("📊 Maritime Port Performance Dashboard (2022–2023)")
st.markdown("""
Welcome to the interactive dashboard that showcases insights from the UNCTAD Maritime Port Performance dataset.
This app helps visualize vessel trends, port efficiency, and key statistics from 2022–2023.
""")

# Insight summary
with st.expander("📌 Summary of EDA Insights"):
    st.markdown("""
    - **Vessel Age**: Average age ~15–18 years. Container and LNG ships tend to be newer.
    - **Time in Port**: Container ships are faster in turnaround; Breakbulk and passenger ships stay longer.
    - **Vessel Size & Capacity**: Larger GT often corresponds with higher cargo (DWT) and container (TEU) capacities.
    - **Period Consistency**: Stable metrics across 2022–2023; no drastic performance shifts.
    """)

# Tabs layout
tab1, tab2, tab3 = st.tabs(["📦 Vessel Type Plots", "🗓 Period Plots", "📈 Correlation Heatmap"])

with tab1:
    st.subheader("Boxplots by Vessel Type")
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    sns.boxplot(x='vessel_type', y='median_time_in_port', data=filtered_df, ax=ax1)
    plt.xticks(rotation=45)
    ax1.set_title("Time in Port by Vessel Type")
    st.pyplot(fig1)

    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.boxplot(x='vessel_type', y='avg_size_GT', data=filtered_df, ax=ax2)
    plt.xticks(rotation=45)
    ax2.set_title("Average Size (GT) by Vessel Type")
    st.pyplot(fig2)

with tab2:
    st.subheader("Boxplots by Period")
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    sns.boxplot(x='period', y='median_time_in_port', data=filtered_df, ax=ax3)
    plt.xticks(rotation=45)
    ax3.set_title("Time in Port by Period")
    st.pyplot(fig3)

    fig4, ax4 = plt.subplots(figsize=(10, 5))
    sns.boxplot(x='period', y='avg_size_GT', data=filtered_df, ax=ax4)
    plt.xticks(rotation=45)
    ax4.set_title("Average Size (GT) by Period")
    st.pyplot(fig4)

with tab3:
    st.subheader("Correlation Heatmap")
    numerical_cols = filtered_df.select_dtypes(include='number')
    fig5, ax5 = plt.subplots(figsize=(12, 10))
    sns.heatmap(numerical_cols.corr(), annot=True, cmap='coolwarm', ax=ax5)
    st.pyplot(fig5)

# Final summary
st.header("📝 Key Findings Recap")
st.markdown("""
- **Container ships** appear most efficient in port time.
- **LNG carriers** show larger average sizes.
- **Operational consistency** was maintained across both years.
- Dataset suitable for clustering or unsupervised ML in future.
""")
