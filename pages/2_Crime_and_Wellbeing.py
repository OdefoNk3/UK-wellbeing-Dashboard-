import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Crime and Wellbeing", layout="wide")
st.title("Crime and Wellbeing: Exploring Trends (2023–2024)")

# ---- DATA ----
data = {
    "Year": [2023, 2024],
    "Total Crimes (Warwickshire)": [49331, 49062],
    "Anxiety Score (West Midlands)": [3.3, 3.1],
    "Happiness Score (West Midlands)": [7.4, 7.6],
    "Life Satisfaction Score (West Midlands)": [7.4, 7.5],
    "Worthwhile Score (West Midlands)": [7.8, 7.8]
}
df = pd.DataFrame(data)
df["Year"] = df["Year"].astype(str)  # convert to string for proper x-axis

# ---- DROPDOWN ----
metric_options = [
    "Anxiety Score (West Midlands)",
    "Happiness Score (West Midlands)",
    "Life Satisfaction Score (West Midlands)",
    "Worthwhile Score (West Midlands)"
]
selected_metric = st.selectbox("Select a Wellbeing Metric:", metric_options)

# ---- % CHANGE CALC ----
crime_change = round((df.iloc[1, 1] - df.iloc[0, 1]) / df.iloc[0, 1] * 100, 2)
metric_change = round((df[selected_metric].iloc[1] - df[selected_metric].iloc[0]) / df[selected_metric].iloc[0] * 100, 2)

# ---- METRICS DISPLAY (TOP) ----
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Total Crimes (2024)", value=f"{df.iloc[1, 1]:,}", delta=f"{crime_change}%", delta_color="inverse")
with col2:
    st.metric(label=f"{selected_metric} (2024)", value=round(df[selected_metric].iloc[1], 2), delta=f"{metric_change}%")

# ---- ZOOMING FOR BAR ----
min_crime = df["Total Crimes (Warwickshire)"].min()
max_crime = df["Total Crimes (Warwickshire)"].max()
zoom_range = [min_crime - 200, max_crime + 200]

# ---- PLOTLY CHART ----
fig = go.Figure()

fig.add_trace(go.Bar(
    x=df["Year"],
    y=df["Total Crimes (Warwickshire)"],
    name="Total Crimes",
    marker_color="skyblue",
    yaxis='y1'
))

fig.add_trace(go.Scatter(
    x=df["Year"],
    y=df[selected_metric],
    name=selected_metric,
    mode='lines+markers',
    marker=dict(color="orange", size=10),
    line=dict(width=3),
    yaxis='y2'
))

fig.update_layout(
    title=dict(
        text=f"<b>Crime Volume vs {selected_metric} (2023–2024)</b>",
        x=0.5,
        xanchor='center'
    ),
    xaxis=dict(
        title="Year",
        type="category",  # ensures clean 2023/2024 labels
    ),
    yaxis=dict(
        title="Total Crimes (Warwickshire)",
        side='left',
        range=zoom_range,
        showgrid=True
    ),
    yaxis2=dict(
        title=selected_metric,
        overlaying='y',
        side='right'
    ),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.2,
        xanchor="center",
        x=0.5
    ),
    margin=dict(t=100, b=80),
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# Divider line and section header
st.markdown("---")
st.subheader("Monthly Crime Trends in Warwickshire (2023 vs 2024)")

import plotly.express as px

st.markdown("---")
st.subheader("📅 Monthly Crime Trends in Warwickshire (2023 vs 2024)")

# ---- Load and process trend data ----
df_trend = pd.read_csv("crime_data_for_trends.csv")  # make sure it's in the same directory

# Ensure Month is datetime
df_trend['Month'] = pd.to_datetime(df_trend['Month'], errors='coerce')

# Extract components
df_trend['Year'] = df_trend['Month'].dt.year
df_trend['Month_Num'] = df_trend['Month'].dt.month
df_trend['Month_Name'] = df_trend['Month'].dt.strftime('%B')

# Group by year and month
monthly_grouped = (
    df_trend
    .groupby(['Year', 'Month_Num', 'Month_Name'])
    .size()
    .reset_index(name='Total Crimes')
    .sort_values(['Year', 'Month_Num'])
)

# Ensure correct month order
month_order = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']
monthly_grouped['Month_Name'] = pd.Categorical(monthly_grouped['Month_Name'], categories=month_order, ordered=True)

# ---- Plotly Line Chart ----
fig_monthly = px.line(
    monthly_grouped,
    x='Month_Name',
    y='Total Crimes',
    color='Year',
    markers=True,
    hover_data=["Total Crimes", "Year"],
    title="📅 Monthly Crime Trends in Warwickshire (2023 vs 2024)",
    labels={"Month_Name": "Month", "Total Crimes": "Total Crimes"},
    category_orders={"Month_Name": month_order},
    color_discrete_map={2023: "royalblue", 2024: "darkorange"}
)

# Improve line style
fig_monthly.update_traces(line=dict(width=3))

# Layout tweaks
fig_monthly.update_layout(
    xaxis_title="Month",
    yaxis_title="Total Crimes",
    legend_title="Year",
    height=500,
    margin=dict(t=80, b=60)
)

# ---- Display in Streamlit ----
st.plotly_chart(fig_monthly, use_container_width=True)

# ---- Insight Summary ----
st.markdown("### 🔍 Insight Summary")
peak_2023 = monthly_grouped[monthly_grouped["Year"] == 2023]["Total Crimes"].max()
peak_2024 = monthly_grouped[monthly_grouped["Year"] == 2024]["Total Crimes"].max()
st.write(
    f"In **2023**, the highest monthly crime total was **{peak_2023:,}**. "
    f"In **2024**, it was **{peak_2024:,}**. This provides a quick view of peak activity across years."
)

import plotly.express as px
import pandas as pd
import streamlit as st

st.markdown("---")
st.subheader("🗺️ Crime Map of Warwickshire by Type")

# Load data
df_map = pd.read_csv("crime_data_for_mapping.csv")  # Ensure this is in the same directory or repo

# Drop missing coordinates
df_map = df_map.dropna(subset=["Latitude", "Longitude"])

# 🎯 FILTER 1: Dropdown for Crime Type
crime_types = sorted(df_map["Crime type"].unique())
selected_type = st.selectbox("Filter by Crime Type:", options=["All"] + crime_types)

if selected_type != "All":
    df_map = df_map[df_map["Crime type"] == selected_type]

# 📊 KPI Summary
st.markdown("### 📊 Map Summary")
st.write(f"Total crimes shown: **{len(df_map):,}**")
st.write(f"Unique crime types in view: **{df_map['Crime type'].nunique()}**")

# 🎨 Custom color palette (qualitative for better contrast)
color_palette = px.colors.qualitative.Set1

# 📍 Create the Map
fig_map = px.scatter_mapbox(
    df_map,
    lat="Latitude",
    lon="Longitude",
    color="Crime type",
    hover_data=["Location", "Crime type", "Month", "Last outcome category"],
    zoom=9,
    height=600,
    title="Crime Locations in Warwickshire (Colored by Crime Type)",
    color_discrete_sequence=color_palette
)

# ✏️ Improve style: dot size, opacity
fig_map.update_traces(marker=dict(size=6, opacity=0.6))

# 🗺️ Final layout polish
fig_map.update_layout(
    mapbox_style="open-street-map",
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
    legend_title_text="Crime Type"
)

# Show map in Streamlit
st.plotly_chart(fig_map, use_container_width=True)
