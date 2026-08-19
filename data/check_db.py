import sqlite3

conn = sqlite3.connect("data/smartinventory.db")

tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print("Tables:", tables)

for table in ["products", "batches", "sales_history"]:
    count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
    print(f"{table}: {count[0]} rows")

conn.close()