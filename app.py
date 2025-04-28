import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("viridis")

# Page configuration
logo_col, title_col = st.columns([1, 4])
with logo_col:
    st.image("https://i.postimg.cc/V6N30WsM/Logo-Round-Image.png", width=110)  
with title_col:
    st.title("📊 Maritime Port Performance Dashboard (2022–2023)")

# Loading the data
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_port_performance_dataset_2022_2023.csv")
    df.columns = df.columns.str.strip().str.lower()  # Normalize to lowercase
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

# KPI Section - USING CORRECT COLUMN NAMES
st.subheader("📌 Key Performance Indicators (KPIs)")
col1, col2, col3 = st.columns(3)

avg_time = filtered_df["median_time_in_port"].mean()
avg_age = filtered_df["avg_vessel_age"].mean()
avg_dwt = filtered_df["avg_cargo_capacity_dwt"].mean()

col1.metric("Avg. Time in Port (Days)", f"{avg_time:.1f}")
col2.metric("Avg. Vessel Age", f"{avg_age:.1f} yrs")
col3.metric("Avg. Cargo Capacity (DWT)", f"{int(avg_dwt):,}")

# ---- Visualization Section ----
st.subheader("📈 Advanced Performance Analysis")

# Plot type selector
plot_type = st.selectbox(
    "Choose Plot Type",
    ["Line Plot", "Bar Chart", "Box Plot", "Scatter Plot"]
)

# Metric selector (updated with DWT)
metric = st.selectbox(
    "Select Metric",
    ["median_time_in_port", "avg_vessel_age", "avg_cargo_capacity_dwt", "avg_size_gt"]
)

# Create tabs for different views
tab1, tab2, tab3 = st.tabs(["Trend Analysis", "Distribution", "Comparison"])

with tab1:
    # Dynamic plot based on selection
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    if plot_type == "Line Plot":
        sns.lineplot(
            data=filtered_df,
            x="period",
            y=metric,
            hue="vessel_type",
            style="vessel_type",
            markers=True,
            ax=ax1
        )
    elif plot_type == "Bar Chart":
        sns.barplot(
            data=filtered_df,
            x="period",
            y=metric,
            hue="vessel_type",
            ax=ax1
        )
    ax1.set_title(f"{plot_type} of {metric.replace('_', ' ').title()}")
    st.pyplot(fig1)

with tab2:
    # Distribution analysis
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.boxplot(
        data=filtered_df,
        x="vessel_type",
        y=metric,
        palette="viridis",
        ax=ax2
    )
    ax2.set_title(f"Distribution by Vessel Type")
    plt.xticks(rotation=45)
    st.pyplot(fig2)

with tab3:
    # Scatter plot comparison
    compare_metric = st.selectbox(
        "Compare With",
        [m for m in ["avg_vessel_age", "avg_size_gt"] if m != metric]
    )
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    sns.scatterplot(
        data=filtered_df,
        x=metric,
        y=compare_metric,
        hue="vessel_type",
        size="avg_size_gt",
        sizes=(20, 200),
        alpha=0.7,
        ax=ax3
    )
    ax3.set_title(f"{metric.replace('_', ' ')} vs {compare_metric.replace('_', ' ')}")
    st.pyplot(fig3)

# Add a histogram below
st.subheader("📊 Metric Distribution")
fig4, ax4 = plt.subplots(figsize=(10, 4))
sns.histplot(
    filtered_df[metric],
    kde=True,
    bins=15,
    color='skyblue',
    ax=ax4
)
ax4.set_xlabel(metric.replace('_', ' ').title())
st.pyplot(fig4)

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