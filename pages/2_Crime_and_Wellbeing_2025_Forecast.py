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

# ---- CRIME FORECAST (ARIMA) ----
st.header("🚓 Forecasted Monthly Crime (2025) — ARIMA Model")
crime_df['Month'] = pd.to_datetime(crime_df['Month'])
crime_df.set_index('Month', inplace=True)
model = SARIMAX(crime_df['Total_Crimes'], order=(1,1,1), seasonal_order=(1,1,1,12))
result = model.fit(disp=False)
future_crime = result.get_forecast(12).predicted_mean
future_index = pd.date_range(start='2025-01-01', periods=12, freq='MS')
future_df = pd.DataFrame({"Month": future_index, "Total_Crimes": future_crime.values})

# COMBINE HISTORICAL + FORECAST
crime_df_reset = crime_df.reset_index()
crime_df_reset['Year'] = crime_df_reset['Month'].dt.year
crime_df_reset['MonthName'] = crime_df_reset['Month'].dt.strftime('%B')
future_df['Year'] = 2025
future_df['MonthName'] = future_df['Month'].dt.strftime('%B')
all_crime = pd.concat([crime_df_reset, future_df])

fig2, ax2 = plt.subplots(figsize=(12, 5))
for year, group in all_crime.groupby("Year"):
    ax2.plot(group['MonthName'], group['Total_Crimes'], marker='o', label=year)

ax2.set_title("Monthly Crime Trends (2023–2025) — ARIMA Forecast", color='white')
ax2.set_ylabel("Total Crimes", color='white')
ax2.set_xlabel("Month", color='white')
ax2.grid(True, linestyle='--', alpha=0.3)
ax2.tick_params(colors='white')
ax2.set_facecolor('#0e1117')
fig2.patch.set_facecolor('#0e1117')
ax2.legend(title='Year', labelcolor='white')
st.pyplot(fig2)

# ---- CRIME TOTALS BAR CHART ----
st.header("📊 Total Crimes Per Year (2025) — ARIMA Forecast")
bar_data = {
    'Year': ['2023', '2024', '2025'],
    'Total Crimes': [49331, 49062, int(future_df['Total_Crimes'].sum())]
}
bar_df = pd.DataFrame(bar_data)
fig3, ax3 = plt.subplots(figsize=(6, 5))
colors = ['#90caf9', '#42a5f5', '#0d47a1']
bars = ax3.bar(bar_df['Year'], bar_df['Total Crimes'], color=colors)

for bar in bars:
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2, height + 50, f"{int(height):,}", ha='center', color='white')

ax3.set_title("Total Crimes Per Year - ARIMA Forecast", color='white')
ax3.set_ylabel("Total Crimes", color='white')
ax3.set_ylim(min(bar_df['Total Crimes']) - 300, max(bar_df['Total Crimes']) + 300)
ax3.grid(axis='y', linestyle='--', alpha=0.3)
ax3.tick_params(colors='white')
ax3.set_facecolor('#0e1117')
fig3.patch.set_facecolor('#0e1117')
st.pyplot(fig3)

# FOOTNOTE
st.caption("Predictions made using: Linear Regression (wellbeing), ARIMA (crime trends)")


# FOOTNOTE
st.caption("Predictions made using: Linear Regression (wellbeing), ARIMA (crime trends)")
