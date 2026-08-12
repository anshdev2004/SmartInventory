import numpy as np
import pandas as pd
from datetime import datetime


def elasticity_demand(Q0: float, P: float, P0: float, epsilon: float) -> float:
    """
    Predicts demand at a new price, given baseline demand at the original price.
    """
    return Q0 * (P / P0) ** (-epsilon)


def time_decay_discount(t_remaining: float, tau: float, D_max: float, alpha: float) -> float:
    """
    Calculates the discount rate (as a fraction, e.g. 0.25 = 25% off) based on
    how many days remain before expiry.
    """
    t_remaining = max(0, min(t_remaining, tau))  # clamp so we never go outside [0, tau]
    return D_max * (1 - t_remaining / tau) ** alpha


def recommended_price(original_price: float, t_remaining: float, tau: float,
                       D_max: float = 0.5, alpha: float = 1.0) -> float:
    """
    Combines the discount into an actual suggested shelf price.
    """
    discount = time_decay_discount(t_remaining, tau, D_max, alpha)
    return round(original_price * (1 - discount), 2)


def generate_markdown_sheet(D_max: float = 0.5, alpha: float = 1.2):
    """
    Reads products.csv and batches.csv, and calculates a recommended
    markdown price for every batch currently in stock.
    """
    products = pd.read_csv("data/products.csv")
    batches = pd.read_csv("data/batches.csv")

    batches["expiry_date"] = pd.to_datetime(batches["expiry_date"])
    today = pd.Timestamp(datetime.today().date())

    merged = batches.merge(products, on="product_id")

    results = []
    for _, row in merged.iterrows():
        days_left = (row["expiry_date"] - today).days
        price = recommended_price(
            original_price=row["original_price"],
            t_remaining=days_left,
            tau=row["shelf_life_days"],
            D_max=D_max,
            alpha=alpha
        )
        results.append({
            "batch_id": row["batch_id"],
            "product": row["name"],
            "days_left": days_left,
            "original_price": row["original_price"],
            "recommended_price": price,
            "discount_%": round((1 - price / row["original_price"]) * 100, 1)
        })

    sheet = pd.DataFrame(results).sort_values("days_left")
    return sheet


if __name__ == "__main__":
    sheet = generate_markdown_sheet()
    print(sheet.to_string(index=False))