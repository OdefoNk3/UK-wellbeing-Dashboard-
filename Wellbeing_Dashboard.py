import streamlit as st
st.set_page_config(page_title="UK Wellbeing Dashboard", layout="wide")

import pandas as pd
import plotly.graph_objects as go

# Load and preprocess original Excel file
@st.cache_data
def load_and_clean_excel(file_path):
    df = pd.read_excel(file_path)
    
    # Detect section headers in 'Year 2023' column
    section_indices = df[df['Year 2023'].astype(str).str.contains('Mean score', na=False)].index.tolist()
    section_indices.append(len(df))  # add end index

    # Extract and clean each block
    sections = []
    for i in range(len(section_indices) - 1):
        start, end = section_indices[i], section_indices[i + 1]
        metric_name = df.loc[start, 'Year 2023'].replace('\n', ' ').strip()
        section = df.iloc[start + 1:end].copy()
        section.columns = ['Demographic', '2023', '2024']
        section.insert(0, 'Category', metric_name)
        section['2023'] = pd.to_numeric(section['2023'], errors='coerce')
        section['2024'] = pd.to_numeric(section['2024'], errors='coerce')
        sections.append(section)
    
    full_data = pd.concat(sections, ignore_index=True)
    return full_data

# Load the dataset
df = load_and_clean_excel("UK Wellbeing census data comparison .xlsx")

# Dashboard layout
st.title("📊 UK Wellbeing Comparison Dashboard (2023 vs 2024)")

# --- Select Metric ---
metric = st.selectbox("1️⃣ Select a Wellbeing Metric", df["Category"].unique())

# Define age group demographics
age_group_demos = [demo for demo in df["Demographic"].unique() if isinstance(demo, str) and "to" in demo]

# --- Multiselect (starts empty) ---
selected_demos = st.multiselect(
    "2️⃣ Select Demographic Groups (optional)",
    options=df["Demographic"].unique(),
    default=[],  # Empty by default (no red pills)
    help="By default, the chart shows age groups. You can select any demographics here to customize the view."
)

# Filter logic
if selected_demos:
    display_df = df[(df["Category"] == metric) & (df["Demographic"].isin(selected_demos))]
else:
    display_df = df[(df["Category"] == metric) & (df["Demographic"].isin(age_group_demos))]

# --- Chart Section ---
fig = go.Figure(data=[
    go.Bar(name='2023', x=display_df['Demographic'], y=display_df['2023'], marker_color='teale'),
    go.Bar(name='2024', x=display_df['Demographic'], y=display_df['2024'], marker_color='orchid')
])

fig.update_layout(
    barmode='group',
    title=f"{metric} Scores by Demographic: 2023 vs 2024",
    xaxis_title="Demographic",
    yaxis_title="Mean Score (out of 10)",
    xaxis_tickangle=-45,
    height=600
)

st.plotly_chart(fig, use_container_width=True)

# --- Download Filtered Data ---
with st.expander("⬇️ Download Filtered Data"):
    st.download_button(
        label="Download as CSV",
        data=display_df.to_csv(index=False),
        file_name=f"{metric}_2023_2024_filtered.csv",
        mime="text/csv"
    )
