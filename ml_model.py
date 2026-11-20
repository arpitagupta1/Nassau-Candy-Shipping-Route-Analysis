
import pandas as pd

# Dataset load karna
df = pd.read_csv("Nassau Candy Distributor.csv")

print("Dataset loaded successfully!")

# Dataset ki basic information
print("\nDataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

# Date conversion
df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    format="%d-%m-%Y",
    errors="coerce"
)

df["Ship Date"] = pd.to_datetime(
    df["Ship Date"],
    format="%d-%m-%Y",
    errors="coerce"
)

# Shipping lead time calculate karna
df["Shipping Lead Time"] = (
    df["Ship Date"] - df["Order Date"]
).dt.days

print("\nShipping Lead Time Summary:")
print(df["Shipping Lead Time"].describe())

print("\nFirst 5 Records:")
print(df[["Order Date", "Ship Date", "Shipping Lead Time"]].head())

# Product ke basis par Factory identify karna

factory_mapping = {
    "Wonka Bar - Nutty Crunch Surprise": "Lot's O' Nuts",
    "Wonka Bar - Fudge Mallows": "Lot's O' Nuts",
    "Wonka Bar -Scrumdiddlyumptious": "Lot's O' Nuts",
    "Wonka Bar - Milk Chocolate": "Wicked Choccy's",
    "Wonka Bar - Triple Dazzle Caramel": "Wicked Choccy's",
    "Laffy Taffy": "Sugar Shack",
    "SweeTARTS": "Sugar Shack",
    "Nerds": "Sugar Shack",
    "Fun Dip": "Sugar Shack",
    "Fizzy Lifting Drinks": "Sugar Shack",
    "Everlasting Gobstopper": "Secret Factory",
    "Hair Toffee": "The Other Factory",
    "Lickable Wallpaper": "Secret Factory",
    "Wonka Gum": "Secret Factory",
    "Kazookles": "The Other Factory"
}

df["Factory"] = df["Product Name"].map(factory_mapping)

print("\nFactory Mapping Results:")
print(df["Factory"].value_counts(dropna=False))

print("\nUnmapped Products:")
print(df.loc[df["Factory"].isna(), "Product Name"].unique())

# Step 6: ML Features Preparation

# Order Date se year aur month nikalna
df["Order Year"] = df["Order Date"].dt.year
df["Order Month"] = df["Order Date"].dt.month

# Machine Learning ke liye features select karna
features = [
    "Factory",
    "State/Province",
    "Region",
    "Ship Mode",
    "Division",
    "Product Name",
    "Sales",
    "Units",
    "Order Year",
    "Order Month"
]

target = "Shipping Lead Time"

# ML dataset banana
ml_data = df[features + [target]].copy()

print("\nML Dataset Shape:")
print(ml_data.shape)

print("\nMissing Values:")
print(ml_data.isnull().sum())

print("\nSelected Features:")
print(features)

print("\nTarget Variable:")
print(target)

# Step 7: Random Forest Regression Model

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
import joblib

# Input features aur target
X = ml_data[features]
y = ml_data[target]

# Categorical aur numerical columns
categorical_features = [
    "Factory",
    "State/Province",
    "Region",
    "Ship Mode",
    "Division",
    "Product Name"
]

numerical_features = [
    "Sales",
    "Units",
    "Order Year",
    "Order Month"
]

# Categorical data ko numerical format mein convert karna
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ("num", "passthrough", numerical_features)
    ]
)

# Random Forest Model
model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("regressor", DecisionTreeRegressor(
    random_state=42
))
    ]
)

# Training aur Testing data split
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

# Model training
model.fit(X_train, y_train)

# Prediction
y_pred = model.predict(X_test)

# Model evaluation
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("\n===== DECISION TREE MODEL RESULTS =====")
print("Training Records:", len(X_train))
print("Testing Records:", len(X_test))
print("MAE:", round(mae, 2), "days")
print("RMSE:", round(rmse, 2), "days")
print("R2 Score:", round(r2, 4))

# Model save karna
joblib.dump(model, "shipping_lead_time_model.pkl")

print("\nModel saved successfully!")

import matplotlib.pyplot as plt

# Actual vs Predicted Graph
plt.figure(figsize=(10, 5))

plt.plot(
    range(50),
    y_test.iloc[:50].values,
    label="Actual Shipping Lead Time",
    marker="o"
)

plt.plot(
    range(50),
    y_pred[:50],
    label="Predicted Shipping Lead Time",
    marker="x"
)

plt.title("Actual vs Predicted Shipping Lead Time")
plt.xlabel("Test Records")
plt.ylabel("Shipping Lead Time (Days)")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig("actual_vs_predicted.png")

plt.show()

print("Graph saved successfully!")

# Step 11: Baseline Model Comparison

from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# Simple baseline model
baseline = DummyRegressor(strategy="mean")

baseline.fit(X_train, y_train)

baseline_pred = baseline.predict(X_test)

# Baseline evaluation
baseline_mae = mean_absolute_error(y_test, baseline_pred)
baseline_r2 = r2_score(y_test, baseline_pred)

print("\n===== MODEL COMPARISON =====")

print("Decision Tree MAE:", round(mae, 2))
print("Baseline MAE:", round(baseline_mae, 2))

print("Decision Tree R2:", round(r2, 4))
print("Baseline R2:", round(baseline_r2, 4))




