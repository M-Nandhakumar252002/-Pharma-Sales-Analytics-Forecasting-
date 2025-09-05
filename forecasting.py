# ==============================
# Pharma Sales Forecasting
# ==============================

# Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from statsmodels.tsa.arima.model import ARIMA
from prophet import Prophet

sns.set()

# ==============================
# Load Data
# ==============================
monthly = pd.read_csv("data/salesmonthly.csv")

# Convert to datetime
monthly["datum"] = pd.to_datetime(monthly["datum"], format="%Y-%m-%d")
monthly.set_index("datum", inplace=True)

# ==============================
# Choose Target Variable
# ==============================
# We forecast on "total_sales"
drug_columns = ["M01AB", "M01AE", "N02BA", "N02BE", "N05B", "N05C", "R03", "R06"]
monthly["total_sales"] = monthly[drug_columns].sum(axis=1)

# ==============================
# ARIMA Forecasting
# ==============================
print("Running ARIMA Forecasting...")

# Split data into train/test
train = monthly["total_sales"][:-12]  # all except last 12 months
test = monthly["total_sales"][-12:]   # last 12 months

# Build ARIMA model
arima_model = ARIMA(train, order=(2,1,2))  # (p,d,q) - can tune
arima_result = arima_model.fit()

# Forecast for next 12 months
arima_forecast = arima_result.forecast(steps=12)

# Plot ARIMA results
plt.figure(figsize=(12, 6))
plt.plot(train.index, train, label="Train")
plt.plot(test.index, test, label="Test", color="orange")
plt.plot(test.index, arima_forecast, label="ARIMA Forecast", color="red")
plt.title("ARIMA Forecast of Total Sales")
plt.xlabel("Date")
plt.ylabel("Sales")
plt.legend()
plt.show()

# ==============================
# Prophet Forecasting
# ==============================
print("Running Prophet Forecasting...")

# Prepare data for Prophet
prophet_df = monthly.reset_index()[["datum", "total_sales"]]
prophet_df.columns = ["ds", "y"]

# Build Prophet model
prophet_model = Prophet(yearly_seasonality=True, daily_seasonality=False)
prophet_model.fit(prophet_df)

# Create future dataframe (24 months ahead)
future = prophet_model.make_future_dataframe(periods=24, freq="M")

# Forecast
forecast = prophet_model.predict(future)

# Plot Prophet results
fig1 = prophet_model.plot(forecast)
plt.title("Prophet Forecast of Total Sales")
plt.show()

fig2 = prophet_model.plot_components(forecast)
plt.show()
