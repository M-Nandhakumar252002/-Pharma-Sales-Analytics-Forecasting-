
# ==============================
# Pharma Sales Time Series Analysis
# ==============================

# Importing libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

# Set seaborn style
sns.set()

# ==============================
# Load Data
# ==============================
hourly = pd.read_csv("data/saleshourly.csv")
daily = pd.read_csv("data/salesdaily.csv")
weekly = pd.read_csv("data/salesweekly.csv")
monthly = pd.read_csv("data/salesmonthly.csv")

# ==============================
# Data Overview
# ==============================
def print_shape(data, name):
    print(f"{name} -> Rows: {data.shape[0]}, Columns: {data.shape[1]}")

print_shape(hourly, "Hourly")
print_shape(daily, "Daily")
print_shape(weekly, "Weekly")
print_shape(monthly, "Monthly")

print("\nSample Data (Hourly):\n", hourly.head(2))
print("\nSample Data (Daily):\n", daily.head(2))
print("\nSample Data (Weekly):\n", weekly.head(2))
print("\nSample Data (Monthly):\n", monthly.head(2))

# ==============================
# Convert Dates
# ==============================
monthly["datum"] = pd.to_datetime(monthly["datum"], format="%Y-%m-%d")
weekly["datum"] = pd.to_datetime(weekly["datum"], format="%m/%d/%Y")
daily["datum"] = pd.to_datetime(daily["datum"], format="%m/%d/%Y")
hourly["datum"] = pd.to_datetime(hourly["datum"], format="%m/%d/%Y %H:%M")

# ==============================
# Monthly Data Preprocessing
# ==============================
monthly["year"] = monthly["datum"].dt.year
monthly["month"] = monthly["datum"].dt.month
monthly["day"] = monthly["datum"].dt.day
monthly.set_index("datum", inplace=True)

# ==============================
# Plot Yearly Sales (Bar Plots)
# ==============================
def plot_yearly_sales(column):
    plt.figure(figsize=(10, 5))
    monthly.groupby("year")[column].mean().plot.bar()
    plt.title(f"Yearly Sales of {column}")
    plt.xlabel("Year")
    plt.ylabel("Sales")
    plt.show()

drug_columns = monthly.columns[0:8]  # first 8 drug categories
for col in drug_columns:
    plot_yearly_sales(col)

# ==============================
# Descriptive Statistics
# ==============================
print("\nMonthly Data Statistics:\n")
print(monthly.describe())

# ==============================
# Plot Line Curves (Monthly Trends)
# ==============================
def plot_line_curve(series, col_name):
    plt.figure(figsize=(15, 5))
    series.plot(kind="line")
    plt.title(f"Monthly Sales of Drug: {col_name}")
    plt.ylabel("Sales")
    plt.show()

for col in drug_columns:
    plot_line_curve(monthly[col], col)

# ==============================
# Daily Data Analysis (Jan 2017 - Feb 2017)
# ==============================
daily["day"] = daily["datum"].dt.day
daily.set_index("datum", inplace=True)

for col in daily.columns[0:8]:
    plot_line_curve(daily[col].loc["2017-01-01":"2017-02-01"], col)

# ==============================
# Total Sales Analysis
# ==============================
monthly["total_sales"] = monthly[drug_columns].sum(axis=1)

plt.figure(figsize=(12, 6))
monthly.groupby("month")["total_sales"].mean().plot.bar(rot=45)
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.title("Average Total Sales of Drugs by Month")
plt.show()
