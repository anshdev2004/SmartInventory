import sqlite3
import pandas as pd

# Load existing CSVs
products = pd.read_csv("data/products.csv")
batches = pd.read_csv("data/batches.csv")
sales_history = pd.read_csv("data/sales_history.csv")

# Connect (this creates the .db file if it doesn't exist yet)
conn = sqlite3.connect("data/smartinventory.db")

# Write each table into the database
products.to_sql("products", conn, if_exists="replace", index=False)
batches.to_sql("batches", conn, if_exists="replace", index=False)
sales_history.to_sql("sales_history", conn, if_exists="replace", index=False)

conn.close()
print("Database created: data/smartinventory.db")
print("Tables: products, batches, sales_history")