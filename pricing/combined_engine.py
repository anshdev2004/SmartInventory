import pandas as pd
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pricing.pricing_engine import time_decay_discount, elasticity_demand
from ml.predict import load_model, predict_demand_for_product


def generate_smart_markdown_sheet(D_max: float = 0.5, alpha: float = 1.2):
    products = pd.read_csv("data/products.csv")
    batches = pd.read_csv("data/batches.csv")
    batches["expiry_date"] = pd.to_datetime(batches["expiry_date"])
    today = pd.Timestamp(datetime.today().date())

    model = load_model()
    merged = batches.merge(products, on="product_id")

    results = []
    for _, row in merged.iterrows():
        days_left = (row["expiry_date"] - today).days

        Q0 = predict_demand_for_product(row["product_id"], datetime.today(), model)

        discount = time_decay_discount(
            t_remaining=days_left,
            tau=row["shelf_life_days"],
            D_max=D_max,
            alpha=alpha
        )
        new_price = round(row["original_price"] * (1 - discount), 2)

        predicted_demand_at_discount = elasticity_demand(
            Q0=Q0,
            P=new_price,
            P0=row["original_price"],
            epsilon=row["elasticity"]
        )

        revenue_no_discount = Q0 * row["original_price"]
        revenue_with_discount = predicted_demand_at_discount * new_price

        results.append({
            "batch_id": row["batch_id"],
            "product": row["name"],
            "days_left": days_left,
            "predicted_Q0": round(Q0, 1),
            "original_price": row["original_price"],
            "recommended_price": new_price,
            "discount_%": round(discount * 100, 1),
            "predicted_demand_at_discount": round(predicted_demand_at_discount, 1),
            "revenue_no_discount": round(revenue_no_discount, 2),
            "revenue_with_discount": round(revenue_with_discount, 2),
        })

    sheet = pd.DataFrame(results).sort_values("days_left")
    return sheet


if __name__ == "__main__":
    sheet = generate_smart_markdown_sheet()
    print(sheet.to_string(index=False))