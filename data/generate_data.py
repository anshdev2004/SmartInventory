import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)  # so results are repeatable every time you run this

# --- 1. Product master list ---
products = pd.DataFrame([
    {"product_id": 1, "name": "Milk",           "category": "Dairy",  "shelf_life_days": 10, "base_price": 3.50, "elasticity": 1.2},
    {"product_id": 2, "name": "Yogurt",         "category": "Dairy",  "shelf_life_days": 14, "base_price": 1.20, "elasticity": 1.0},
    {"product_id": 3, "name": "Bread",          "category": "Bakery", "shelf_life_days": 4,  "base_price": 2.80, "elasticity": 1.5},
    {"product_id": 4, "name": "Croissant",      "category": "Bakery", "shelf_life_days": 3,  "base_price": 1.80, "elasticity": 1.6},
    {"product_id": 5, "name": "Bananas",        "category": "Produce","shelf_life_days": 6,  "base_price": 0.60, "elasticity": 1.3},
    {"product_id": 6, "name": "Tomatoes",       "category": "Produce","shelf_life_days": 8,  "base_price": 2.20, "elasticity": 1.1},
    {"product_id": 7, "name": "Lettuce",        "category": "Produce","shelf_life_days": 5,  "base_price": 1.50, "elasticity": 1.4},
    {"product_id": 8, "name": "Chicken Breast", "category": "Meat",   "shelf_life_days": 4,  "base_price": 6.50, "elasticity": 0.9},
    {"product_id": 9, "name": "Ground Beef",    "category": "Meat",   "shelf_life_days": 3,  "base_price": 7.00, "elasticity": 0.8},
    {"product_id": 10,"name": "Canned Beans",   "category": "Pantry", "shelf_life_days": 180,"base_price": 1.00, "elasticity": 0.5},
])

# --- 2. Generate daily sales history (last 90 days) ---
start_date = datetime.today() - timedelta(days=90)
dates = [start_date + timedelta(days=i) for i in range(90)]

sales_records = []
for _, prod in products.iterrows():
    base_demand = np.random.randint(15, 60)
    for d in dates:
        weekend_boost = 1.3 if d.weekday() >= 5 else 1.0
        noise = np.random.normal(1.0, 0.15)
        units_sold = max(0, int(base_demand * weekend_boost * noise))
        sales_records.append({
            "product_id": prod["product_id"],
            "date": d.strftime("%Y-%m-%d"),
            "units_sold": units_sold
        })

sales_history = pd.DataFrame(sales_records)

# --- 3. Generate current batch stock (what's on the shelf right now) ---
batch_records = []
batch_id = 1
for _, prod in products.iterrows():
    num_batches = np.random.randint(2, 4)
    for _ in range(num_batches):
        days_since_manufacture = np.random.randint(0, prod["shelf_life_days"])
        manufacture_date = datetime.today() - timedelta(days=days_since_manufacture)
        expiry_date = manufacture_date + timedelta(days=prod["shelf_life_days"])
        batch_records.append({
            "batch_id": batch_id,
            "product_id": prod["product_id"],
            "manufacture_date": manufacture_date.strftime("%Y-%m-%d"),
            "expiry_date": expiry_date.strftime("%Y-%m-%d"),
            "quantity": np.random.randint(10, 80),
            "original_price": prod["base_price"]
        })
        batch_id += 1

batches = pd.DataFrame(batch_records)

# --- 4. Save everything to CSV ---
products.to_csv("data/products.csv", index=False)
sales_history.to_csv("data/sales_history.csv", index=False)
batches.to_csv("data/batches.csv", index=False)

print("Done. Files created:")
print(" - data/products.csv       (10 products)")
print(" - data/sales_history.csv  (90 days of sales per product)")
print(" - data/batches.csv        (current stock batches)")