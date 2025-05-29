import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ---- PAGE CONFIG ----
st.title("Crime and Wellbeing: Exploring Trends (2023–2024)")

# ---- FINAL DATA ----
data = {
    "Year": [2023, 2024],
    "Total Crimes (Warwickshire)": [49331, 49062],
    "Anxiety Score (West Midlands)": [3.3, 3.1],
    "Happiness Score (West Midlands)": [7.4, 7.6],
    "Life Satisfaction Score (West Midlands)": [7.4, 7.5],
    "Worthwhile Score (West Midlands)": [7.8, 7.8]
}
df = pd.DataFrame(data)

# Convert Year to string to fix x-axis
df["Year"] = df["Year"].astype(str)

# ---- DROPDOWN SELECTION ----
metric_options = [
    "Anxiety Score (West Midlands)",
    "Happiness Score (West Midlands)",
    "Life Satisfaction Score (West Midlands)",
    "Worthwhile Score (West Midlands)"
]
selected_metric = st.selectbox("Select Wellbeing Metric:", metric_options)

# ---- % CHANGE CALCULATION ----
crime_pct_change = round(((df.loc[1, "Total Crimes (Warwickshire)"] - df.loc[0, "Total Crimes (Warwickshire)"]) / df.loc[0, "Total Crimes (Warwickshire)"]) * 100, 2)
metric_pct_change = round(((df.loc[1, selected_metric] - df.loc[0, selected_metric]) / df.loc[0, selected_metric]) * 100, 2)

# ---- COMBINED CHART ----
fig = go.Figure()

# Bar chart for Total Crimes
fig.add_trace(go.Bar(
    x=df["Year"],
    y=df["Total Crimes (Warwickshire)"],
    name="Total Crimes",
    marker_color="skyblue",
    yaxis='y1'
))

# Line chart for selected wellbeing metric
fig.add_trace(go.Scatter(
    x=df["Year"],
    y=df[selected_metric],
    name=selected_metric,
    marker=dict(color="darkorange", size=10),
    line=dict(width=3),
    mode='lines+markers',
    yaxis='y2'
))

# Zoom in on Total Crimes y-axis
min_crime = df["Total Crimes (Warwickshire)"].min()
max_crime = df["Total Crimes (Warwickshire)"].max()
crime_padding = 500

# Layout update
fig.update_layout(
    title=f"<b>Crime Volume vs {selected_metric} (2023–2024)</b>",
    xaxis=dict(title="Year"),
    yaxis=dict(title="Total Crimes (Warwickshire)", side='left', range=[min_crime - crime_padding, max_crime + crime_padding]),
    yaxis2=dict(title=selected_metric, overlaying='y', side='right'),
    legend=dict(x=0.01, y=1.15, orientation="h"),
    height=500,
    margin=dict(t=80, b=50),
)

# Show chart
st.plotly_chart(fig, use_container_width=True)

# ---- METRIC DISPLAY BELOW CHART ----
st.markdown("### Year-on-Year % Change")
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Crime (Warwickshire)", value=f"{df.loc[1, 'Total Crimes (Warwickshire)']:,}", delta=f"{crime_pct_change}%")
with col2:
    st.metric(label=selected_metric, value=round(df.loc[1, selected_metric], 2), delta=f"{metric_pct_change}%")

