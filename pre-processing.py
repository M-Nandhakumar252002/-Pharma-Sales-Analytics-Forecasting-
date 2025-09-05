"""
Data Preprocessing for Pharma Sales Daily Data
Libraries: pandas, numpy
"""

import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv("salesdaily.csv")

# -------------------------------
# Step 1: Basic dataset inspection
# -------------------------------
print("Dataset Shape:", df.shape)
print("\nColumn Info:")
print(df.info())
print("\nMissing values per column:")
print(df.isnull().sum())

# -------------------------------
# Step 2: Handle missing values
# -------------------------------
# Numeric columns → replace NaN with column mean
numeric_cols = df.select_dtypes(include=[np.number]).columns
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

# Categorical columns → replace NaN with mode
categorical_cols = df.select_dtypes(include=["object"]).columns
for col in categorical_cols:
    df[col] = df[col].fillna(df[col].mode()[0])

# -------------------------------
# Step 3: Date and Time Features
# -------------------------------
if "datum" in df.columns:
    df["datum"] = pd.to_datetime(df["datum"], errors="coerce")
    df["Year"] = df["datum"].dt.year
    df["Month"] = df["datum"].dt.month
    df["Day"] = df["datum"].dt.day
    df["Weekday"] = df["datum"].dt.day_name()
    df["Quarter"] = df["datum"].dt.quarter

# -------------------------------
# Step 4: Feature Engineering
# -------------------------------
# Total sales across all categories
drug_cols = ["M01AB", "M01AE", "N02BA", "N02BE", "N05B", "N05C", "R03", "R06"]
df["Total_Sales"] = df[drug_cols].sum(axis=1)

# Relative contribution of each drug per day
for col in drug_cols:
    df[f"{col}_Share"] = df[col] / df["Total_Sales"]

# -------------------------------
# Step 5: Outlier detection
# -------------------------------
# Z-score based removal for Total_Sales
df["z_score_sales"] = (df["Total_Sales"] - df["Total_Sales"].mean()) / df["Total_Sales"].std()
outliers = df[df["z_score_sales"].abs() > 3]
print("\nOutliers detected (|z|>3):", outliers.shape[0])

# Optionally remove outliers
df_clean = df[df["z_score_sales"].abs() <= 3].copy()

# -------------------------------
# Step 6: Final dataset check
# -------------------------------
print("\nProcessed Dataset Shape:", df_clean.shape)
print("\nSample rows:")
print(df_clean.head())

# Save processed file
df_clean.to_csv("salesdaily_processed.csv", index=False)
