import pandas as pd
from xgboost import XGBRegressor
from datetime import datetime, timedelta

def load_model():
    model = XGBRegressor()
    model.load_model("ml/demand_model.json")
    return model


def predict_demand_for_product(product_id: int, target_date: datetime, model) -> float:
    """
    Predicts expected units sold for a given product on a given date,
    using the most recent 7 days of actual sales history to build the rolling average.
    """
    sales = pd.read_csv("data/sales_history.csv")
    sales["date"] = pd.to_datetime(sales["date"])

    # Get this product's most recent 7 days of sales (before target_date)
    recent = sales[
        (sales["product_id"] == product_id) & (sales["date"] < target_date)
    ].sort_values("date").tail(7)

    if recent.empty:
        raise ValueError(f"No historical sales data found for product_id {product_id}")

    rolling_avg_7d = recent["units_sold"].mean()
    day_of_week = target_date.weekday()
    is_weekend = 1 if day_of_week >= 5 else 0

    features = pd.DataFrame([{
        "product_id": product_id,
        "day_of_week": day_of_week,
        "is_weekend": is_weekend,
        "rolling_avg_7d": rolling_avg_7d
    }])

    prediction = model.predict(features)[0]
    return max(0, round(prediction, 1))  # sales can't be negative


if __name__ == "__main__":
    model = load_model()
    tomorrow = datetime.today() + timedelta(days=1)

    products = pd.read_csv("data/products.csv")
    print(f"Predicted demand for {tomorrow.strftime('%Y-%m-%d')}:\n")
    for _, prod in products.iterrows():
        demand = predict_demand_for_product(prod["product_id"], tomorrow, model)
        # print(f"  {prod['name']:<15} -> {demand:.if} units")
        print(f"  {prod['name']:<15} -> {demand:.1f} units")