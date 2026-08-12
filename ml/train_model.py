import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# --- 1. Load data ---
sales = pd.read_csv("data/sales_history.csv")
sales["date"] = pd.to_datetime(sales["date"])
sales = sales.sort_values(["product_id", "date"])

# --- 2. Feature engineering ---
sales["day_of_week"] = sales["date"].dt.dayofweek
sales["is_weekend"] = (sales["day_of_week"] >= 5).astype(int)

# Rolling 7-day average sales, per product, using only PAST data (shift by 1 to avoid leaking today's answer)
sales["rolling_avg_7d"] = (
    sales.groupby("product_id")["units_sold"]
    .transform(lambda x: x.shift(1).rolling(window=7, min_periods=1).mean())
)

# Drop early rows where rolling average couldn't be computed yet
sales = sales.dropna(subset=["rolling_avg_7d"])

# --- 3. Define features (X) and target (y) ---
feature_cols = ["product_id", "day_of_week", "is_weekend", "rolling_avg_7d"]
X = sales[feature_cols]
y = sales["units_sold"]

# --- 4. Train/test split (80% train, 20% test, keep it simple with random split for now) ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- 5. Train the model ---
model = XGBRegressor(n_estimators=100, max_depth=4, learning_rate=0.1, random_state=42)
model.fit(X_train, y_train)

# --- 6. Evaluate ---
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
print(f"Model trained. Mean Absolute Error: {mae:.2f} units")

# --- 7. Save the trained model for later use ---
model.save_model("ml/demand_model.json")
print("Model saved to ml/demand_model.json")