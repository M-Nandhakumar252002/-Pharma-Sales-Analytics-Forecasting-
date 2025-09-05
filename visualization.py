"""
Data Visualization for Pharma Sales Daily Data
Libraries: pandas, matplotlib, seaborn
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load processed data
df = pd.read_csv("salesdaily_processed.csv")

# -------------------------------
# Style settings
# -------------------------------
sns.set_theme(style="whitegrid", palette="muted")

# -------------------------------
# 1. Distribution of Total Sales
# -------------------------------
plt.figure(figsize=(10,6))
sns.histplot(df["Total_Sales"], bins=30, kde=True)
plt.title("Distribution of Daily Total Sales", fontsize=14)
plt.xlabel("Total Sales")
plt.ylabel("Frequency")
plt.show()

# -------------------------------
# 2. Monthly Sales Trend
# -------------------------------
monthly_sales = df.groupby(["Year", "Month"])["Total_Sales"].sum().reset_index()
plt.figure(figsize=(12,6))
sns.lineplot(data=monthly_sales, x="Month", y="Total_Sales", hue="Year", marker="o")
plt.title("Monthly Total Sales Trend", fontsize=14)
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.show()

# -------------------------------
# 3. Drug-wise Average Sales
# -------------------------------
drug_cols = ["M01AB", "M01AE", "N02BA", "N02BE", "N05B", "N05C", "R03", "R06"]
avg_sales = df[drug_cols].mean().reset_index()
avg_sales.columns = ["Drug", "Average_Sales"]

plt.figure(figsize=(10,6))
sns.barplot(data=avg_sales, x="Drug", y="Average_Sales")
plt.title("Average Sales by Drug Category", fontsize=14)
plt.ylabel("Average Daily Sales")
plt.show()

# -------------------------------
# 4. Sales by Weekday
# -------------------------------
plt.figure(figsize=(10,6))
sns.boxplot(data=df, x="Weekday", y="Total_Sales", order=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
plt.title("Sales Distribution by Weekday", fontsize=14)
plt.xticks(rotation=45)
plt.show()

# -------------------------------
# 5. Correlation Heatmap
# -------------------------------
plt.figure(figsize=(10,6))
sns.heatmap(df[drug_cols + ["Total_Sales"]].corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap of Drug Categories and Total Sales", fontsize=14)
plt.show()

# -------------------------------
# 6. Seasonal Analysis
# -------------------------------
df["Season"] = pd.cut(df["Month"], bins=[0,2,5,8,11,12],
                      labels=["Winter","Spring","Summer","Fall","Winter"], include_lowest=True)

seasonal_sales = df.groupby("Season")["Total_Sales"].mean().reset_index()
plt.figure(figsize=(8,6))
sns.barplot(data=seasonal_sales, x="Season", y="Total_Sales", order=["Winter","Spring","Summer","Fall"])
plt.title("Average Sales by Season", fontsize=14)
plt.show()

# -------------------------------
# 7. Forecasting with Rolling Average
# -------------------------------

# Prepare monthly sales time series
monthly_sales = df.groupby(["Year", "Month"])["Total_Sales"].sum().reset_index()
monthly_sales["Date"] = pd.to_datetime(monthly_sales["Year"].astype(str) + "-" + monthly_sales["Month"].astype(str) + "-01")

# Sort just in case
monthly_sales = monthly_sales.sort_values("Date")

# Rolling average (window = 3 months)
monthly_sales["Rolling_Avg"] = monthly_sales["Total_Sales"].rolling(window=3, min_periods=1).mean()

# Plot actual vs rolling average
plt.figure(figsize=(12,6))
plt.plot(monthly_sales["Date"], monthly_sales["Total_Sales"], marker="o", label="Actual Sales")
plt.plot(monthly_sales["Date"], monthly_sales["Rolling_Avg"], color="red", linestyle="--", label="3-Month Rolling Avg")
plt.title("Monthly Sales with Rolling Average", fontsize=14)
plt.xlabel("Date")
plt.ylabel("Total Sales")
plt.legend()
plt.grid(True)
plt.show()

# -------------------------------
# 8. Simple Forecast Projection
# -------------------------------

# Forecast next 6 months using last 3-month average
last_avg = monthly_sales["Total_Sales"].tail(3).mean()

# Create 6 future months
last_date = monthly_sales["Date"].max()
future_dates = pd.date_range(start=last_date + pd.offsets.MonthBegin(1), periods=6, freq="MS")
future_forecast = pd.DataFrame({"Date": future_dates, "Forecast": [last_avg]*6})

# Plot historical + forecast
plt.figure(figsize=(12,6))
plt.plot(monthly_sales["Date"], monthly_sales["Total_Sales"], marker="o", label="Historical Sales")
plt.plot(future_forecast["Date"], future_forecast["Forecast"], marker="x", linestyle="--", color="red", label="Forecast (Next 6 Months)")
plt.title("Sales Forecast (Simple Moving Avg Projection)", fontsize=14)
plt.xlabel("Date")
plt.ylabel("Total Sales")
plt.legend()
plt.grid(True)
plt.show()
