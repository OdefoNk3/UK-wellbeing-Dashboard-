import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="Crime and UK Wellbeing Trends",
    page_icon="📊",
    layout="wide"
)

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
df["Year"] = df["Year"].astype(str)

# ---- WELLBEING METRIC SELECTION ----
metric_options = [
    "Anxiety Score (West Midlands)",
    "Happiness Score (West Midlands)",
    "Life Satisfaction Score (West Midlands)",
    "Worthwhile Score (West Midlands)"
]
selected_metric = st.selectbox("Select a Wellbeing Metric:", metric_options)

# ---- YEAR TOGGLE FOR KPI ----
selected_year = st.radio("Select Year to Display:", options=["2023", "2024"], horizontal=True)
selected_year = int(selected_year)
selected_idx = df[df["Year"] == str(selected_year)].index[0]

# ---- METRIC VALUES ----
crime_value = df.loc[selected_idx, "Total Crimes (Warwickshire)"]
metric_value = df.loc[selected_idx, selected_metric]

# ---- % CHANGE CALCULATIONS ----
crime_pct_change = round((df.loc[1, "Total Crimes (Warwickshire)"] - df.loc[0, "Total Crimes (Warwickshire)"]) / df.loc[0, "Total Crimes (Warwickshire)"] * 100, 2)
metric_pct_change = round((df[selected_metric].iloc[1] - df[selected_metric].iloc[0]) / df[selected_metric].iloc[0] * 100, 2)

# ---- KPI METRICS DISPLAY ----
col1, col2 = st.columns(2)
with col1:
    st.metric(label=f"Total Crimes ({selected_year})", value=f"{int(crime_value):,}", delta=f"{crime_pct_change}%", delta_color="inverse")
with col2:
    st.metric(label=f"{selected_metric} ({selected_year})", value=round(metric_value, 2), delta=f"{metric_pct_change}%")

# ---- CHART ZOOM RANGE ----
min_crime = df["Total Crimes (Warwickshire)"].min()
max_crime = df["Total Crimes (Warwickshire)"].max()
zoom_range = [min_crime - 200, max_crime + 200]

# ---- COLOR SETTINGS ----
bar_colors = ["#FF69B4", "#A569BD"]  # 2023: hot pink, 2024: purple
line_color = "#00CED1"  # turquoise

# ---- PLOTLY CHART ----
fig = go.Figure()

# Bar for 2023 (Pink)
fig.add_trace(go.Bar(
    x=["2023"],
    y=[df.loc[df["Year"] == "2023", "Total Crimes (Warwickshire)"].values[0]],
    name="2023 Total Crimes",
    marker_color="#FF69B4",
    yaxis='y1'
))

# Bar for 2024 (Purple)
fig.add_trace(go.Bar(
    x=["2024"],
    y=[df.loc[df["Year"] == "2024", "Total Crimes (Warwickshire)"].values[0]],
    name="2024 Total Crimes",
    marker_color="#A569BD",
    yaxis='y1'
))


# Wellbeing Metric Line
fig.add_trace(go.Scatter(
    x=df["Year"],
    y=df[selected_metric],
    name=selected_metric,
    mode='lines+markers',
    marker=dict(color=line_color, size=10),
    line=dict(color=line_color, width=3),
    yaxis='y2'
))

# Layout
fig.update_layout(
    title=dict(text=f"<b>Crime Volume vs {selected_metric} (2023–2024)</b>", x=0.5, font=dict(size=18)),
    xaxis=dict(title="Year", type="category"),
    yaxis=dict(title="Total Crimes (Warwickshire)", side='left', range=zoom_range),
    yaxis2=dict(title=selected_metric, overlaying='y', side='right'),
    legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5),
    margin=dict(t=100, b=80),
    height=500
)

# Display chart
st.plotly_chart(fig, use_container_width=True)


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
    color_discrete_map={2023: "#FF69B4", 2024: "#00CED1"}
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

# Load the data
df_map = pd.read_csv("crime_data_for_mapping.csv")
df_map = df_map.dropna(subset=["Latitude", "Longitude"])

# Get all crime types
all_crime_types = sorted(df_map["Crime type"].unique())

# 🎨 New vibrant color palette (15 high-contrast colors)
vibrant_colors = [
    "#e6194b", "#3cb44b", "#ffe119", "#4363d8", "#f58231",
    "#911eb4", "#46f0f0", "#f032e6", "#bcf60c", "#fabebe",
    "#008080", "#e6beff", "#9a6324", "#fffac8", "#800000"
]

# Create a fixed color map
color_map = {crime: vibrant_colors[i % len(vibrant_colors)] for i, crime in enumerate(all_crime_types)}

# Filter dropdown
selected_type = st.selectbox("Filter by Crime Type:", options=["All"] + all_crime_types)

# Filter data
filtered_df = df_map if selected_type == "All" else df_map[df_map["Crime type"] == selected_type]

# 📊 KPI Summary
st.markdown("### 📊 Map Summary")
st.write(f"Total crimes shown: **{len(filtered_df):,}**")
st.write(f"Unique crime types in view: **{filtered_df['Crime type'].nunique()}**")

# 📍 Map
fig_map = px.scatter_mapbox(
    filtered_df,
    lat="Latitude",
    lon="Longitude",
    color="Crime type",
    hover_data=["Location", "Crime type", "Month", "Last outcome category"],
    zoom=9,
    height=600,
    title="Crime Locations in Warwickshire (Colored by Crime Type)",
    color_discrete_map=color_map
)

fig_map.update_traces(marker=dict(size=6, opacity=0.65))
fig_map.update_layout(
    mapbox_style="open-street-map",
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
    legend_title_text="Crime Type"
)

st.plotly_chart(fig_map, use_container_width=True)

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.markdown("---")
st.subheader("📊 Types of Crime Committed in Warwickshire (2023 vs 2024)")

# Load and prepare data
df = pd.read_csv("crime_data_for_trends.csv")
df["Year"] = pd.to_datetime(df["Month"], errors="coerce").dt.year
df = df[df["Year"].isin([2023, 2024])].dropna(subset=["Crime type"])

# Count crimes per type and year
crime_counts = df.groupby(["Crime type", "Year"]).size().unstack(fill_value=0).reset_index()
crime_counts["% Change"] = round(((crime_counts[2024] - crime_counts[2023]) / crime_counts[2023]) * 100, 2)
crime_counts = crime_counts.sort_values(by=2024, ascending=False)

# Toggle between Dot Plot and Grouped Bar Chart
chart_type = st.radio("Select chart type:", ["Dot Plot", "Grouped Bar Chart"])

if chart_type == "Dot Plot":
    fig = go.Figure()
    for _, row in crime_counts.iterrows():
        fig.add_trace(go.Scatter(
            x=[row[2023], row[2024]],
            y=[row["Crime type"]] * 2,
            mode='lines',
            line=dict(color='gray', width=1, dash='dot'),
            showlegend=False
        ))

    fig.add_trace(go.Scatter(
        x=crime_counts[2023],
        y=crime_counts["Crime type"],
        mode='markers',
        name='2023',
        marker=dict(color='#FF69B4', size=9),
        customdata=crime_counts["% Change"],
        hovertemplate='2023<br>%{y}: %{x}<br>Change to 2024: %{customdata:.2f}%<extra></extra>'
    ))

    fig.add_trace(go.Scatter(
        x=crime_counts[2024],
        y=crime_counts["Crime type"],
        mode='markers',
        name='2024',
        marker=dict(color='#00CED1', size=11, line=dict(width=2, color='black')),
        customdata=crime_counts["% Change"],
        hovertemplate='2024<br>%{y}: %{x}<br>Change from 2023: %{customdata:.2f}%<extra></extra>'
    ))

    fig.update_layout(
        title="Dot Plot: Crime Totals per Type in 2023 vs 2024",
        xaxis_title="Total Crimes",
        yaxis_title="Crime Type",
        height=750,
        margin=dict(t=80, b=60),
        legend_title_text="Year",
        yaxis=dict(automargin=True, categoryorder="total ascending"),
        plot_bgcolor='rgba(0,0,0,0)'
    )

else:
    crime_long = crime_counts.melt(
        id_vars=["Crime type", "% Change"],
        value_vars=[2023, 2024],
        var_name="Year",
        value_name="Total Crimes"
    )
    crime_long["Year"] = crime_long["Year"].astype(str)

    fig = px.bar(
        crime_long,
        x="Total Crimes",
        y="Crime type",
        color="Year",
        orientation="h",
        barmode="group",
        title="Grouped Bar Chart: Crime Totals by Type (2023 vs 2024)",
        hover_data={"% Change": True, "Total Crimes": True, "Year": True},
        color_discrete_map={"2023": "#FF69B4", "2024": "#00CED1"}
    )

    fig.update_layout(
        xaxis_title="Total Crimes",
        yaxis_title="Crime Type",
        height=750,
        margin=dict(t=80, b=60),
        legend_title_text="Year"
    )

# Show chart and insights
col1, col2 = st.columns([3, 1])
with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    most_increased = crime_counts.loc[crime_counts["% Change"].idxmax()]
    most_decreased = crime_counts.loc[crime_counts["% Change"].idxmin()]

    st.markdown("### 🔍 Key Insights")
    st.markdown(
        f"<span style='color:green'>🟢 <strong>Highest Increase</strong></span>: "
        f"`{most_increased['Crime type']}` increased by <span style='color:green'>"
        f"{most_increased['% Change']}%</span> from 2023 to 2024.",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<span style='color:red'>🔴 <strong>Biggest Drop</strong></span>: "
        f"`{most_decreased['Crime type']}` decreased by <span style='color:red'>"
        f"{most_decreased['% Change']}%</span> from 2023 to 2024.",
        unsafe_allow_html=True
    )

