import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.statespace.sarimax import SARIMAX

# PAGE CONFIG
st.set_page_config(page_title="Crime and Wellbeing 2025 Forecast", layout="wide")
st.title("📊 Crime and Wellbeing 2025 Forecast")
st.markdown("---")

# PAGE NAVIGATION INFO
st.info("This page presents 2025 forecasted values for wellbeing and crime. Models used: Linear Regression (for wellbeing scores) and ARIMA (for monthly and total crime projections).")

# ---- DATA LOADING ----
crime_file = "data/warwickshire_total_crime_by_months_trends.xlsx"
wellbeing_file = "data/Final_Corrected_Crime_and_Wellbeing_Comparison.xlsx"

crime_df = pd.read_excel(crime_file)
wellbeing_df = pd.read_excel(wellbeing_file)

# ---- WELLBEING FORECAST ----
st.header("🧠 Forecasted Wellbeing Scores (2025) — Linear Regression")
wellbeing_vars = [
    "Anxiety Score (West Midlands)",
    "Happiness Score (West Midlands)",
    "Life Satisfaction Score (West Midlands)",
    "Worthwhile Score (West Midlands)"
]
X = wellbeing_df[["Year"]]
future = pd.DataFrame({"Year": [2025]})
predicted_data = {"Year": [2023, 2024, 2025]}
for var in wellbeing_vars:
    model = LinearRegression().fit(X, wellbeing_df[[var]])
    pred = model.predict(future)[0][0]
    predicted_data[var] = list(wellbeing_df[var]) + [pred]

forecast_df = pd.DataFrame(predicted_data)
plot_df = forecast_df.set_index("Year").T

fig1, ax1 = plt.subplots(figsize=(10, 5))
plot_df.plot(kind='bar', ax=ax1, color=['#90caf9', '#42a5f5', '#0d47a1'], edgecolor='white')
ax1.set_title("Forecasted Wellbeing Scores in the West Midlands (2023–2025)", color='white')
ax1.set_ylabel("Score (0–10)", color='white')
ax1.set_ylim(0, 10)
ax1.grid(axis='y', linestyle='--', alpha=0.3)
ax1.tick_params(colors='white')
ax1.set_facecolor('#0e1117')
fig1.patch.set_facecolor('#0e1117')
ax1.legend(title="Year", loc='lower right', labelcolor='white')
for container in ax1.containers:
    ax1.bar_label(container, fmt='%.1f', label_type='edge', padding=3, color='white')
st.pyplot(fig1)







